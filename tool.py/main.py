import os,sys,time

class ContainerNotFoundError(Exception):
    """Raised when a referenced container (or container path) is not found."""
    pass

class Display:
    def __init__(self):
        # get terminal size
        self.tx = os.get_terminal_size().columns
        self.ty = os.get_terminal_size().lines
        self.terminal = [[' ' for _ in range(self.tx)] for _ in range(self.ty)]
        self.last_terminal = [[' ' for _ in range(self.tx)] for _ in range(self.ty)]
        self.objects = []
        # buffering / freeze control
        self.frozen = False
        self._pending_output = []
        self._cursor_hidden = False

    def _write(self, s: str):
        # buffer when frozen; write-through otherwise
        if self.frozen:
            self._pending_output.append(s)
        else:
            sys.stdout.write(s)

    def flush(self):
        # flush buffered output in one go
        if self._pending_output:
            sys.stdout.write(''.join(self._pending_output))
            self._pending_output.clear()
        sys.stdout.flush()

    def freeze(self):
        if not self.frozen:
            self.frozen = True
            # hide cursor immediately to reduce flicker
            if not self._cursor_hidden:
                sys.stdout.write("\x1b[?25l")
                sys.stdout.flush()
                self._cursor_hidden = True

    def unfreeze(self):
        if self.frozen:
            # emit everything at once
            self.flush()
            self.frozen = False
            # show cursor back
            if self._cursor_hidden:
                sys.stdout.write("\x1b[?25h")
                sys.stdout.flush()
                self._cursor_hidden = False

    def update(self):
        # compare old content and new content, replace specific location of terminal (which has been changed) to new one
        for lc in range(self.ty):
            line_changed = False
            for cc in range(self.tx):
                if self.terminal[lc][cc] != self.last_terminal[lc][cc]:
                    line_changed = True
                    break
            if line_changed:
                # move cursor to (lc,0)
                self._write(f"\x1b[{lc+1};1H")
                # write the whole line
                self._write(''.join(self.terminal[lc]))
        # only flush immediately when not frozen
        if not self.frozen:
            sys.stdout.flush()

    def calculate_objects(self):
        pass

    def container(self,bx,by,ex,ey,name):
        # make container to put some objects in
        # coordinate convention: (bx,by) and (ex,ey) are inclusive screen coordinates
        # name is used to reference this container from text.container (supports nesting)
        self.objects += [{'type':'container','bx':bx,'by':by,'ex':ex,'ey':ey,'name':name}]

    def text(self,content,x,y,container=[],maxlines=1,maxlength=1000):
        # make text object
        # self.objects.append({'type':'text','content':content,'x':x,'y':y,'maxlines':maxlines,'maxlength':maxlength})
        self.objects.append({'type':'text','content':content,'x':x,'y':y,'maxlines':maxlines,'maxlength':maxlength,'container':container})

    def render(self):
        # clear terminal content
        self.terminal = [[' ' for _ in range(self.tx)] for _ in range(self.ty)]

        # 1) Collect containers for this frame. We don't render them; they define regions only.
        containers = [o for o in self.objects if o.get('type') == 'container']

        # helper: find a container by name, optionally ensuring it's inside a bounding rect
        def find_container(name, within_rect=None):
            for c in containers:
                if c.get('name') != name:
                    continue
                if within_rect is None:
                    return c
                # ensure containment: candidate must be fully inside 'within_rect'
                if (c['bx'] >= within_rect['bx'] and c['by'] >= within_rect['by'] and
                    c['ex'] <= within_rect['ex'] and c['ey'] <= within_rect['ey']):
                    return c
            return None

        # display rect (used when no container path is provided)
        display_rect = {'bx': 0, 'by': 0, 'ex': self.tx - 1, 'ey': self.ty - 1}

        # 2) Render all non-container objects
        for obj in self.objects:
            if obj['type'] == 'container':
                # skip containers; they are only reference frames
                continue

            if obj['type'] == 'text':
                # resolve container path (left-to-right): display -> a -> b -> c
                rect = display_rect
                path = obj.get('container') or []
                if isinstance(path, str):
                    path = [path]

                for name in path:
                    next_rect = find_container(name, within_rect=rect)
                    if not next_rect:
                        # include path context for easier debugging
                        raise ContainerNotFoundError(f"Container '{name}' not found within {rect} (path={path})")
                    rect = next_rect  # descend into the next container

                # compute base offset from the deepest container (or display)
                base_x, base_y = rect['bx'], rect['by']
                max_x, max_y = rect['ex'], rect['ey']

                # break content into lines by maxlength, then cap by maxlines
                lines = []
                content = obj['content']
                while len(content) > obj['maxlength']:
                    lines.append(content[:obj['maxlength']])
                    content = content[obj['maxlength']:]
                lines.append(content)
                lines = lines[:obj['maxlines']]

                # draw with clipping to the container rect and display bounds
                for i, line in enumerate(lines):
                    dy = base_y + obj['y'] + i
                    if dy < 0 or dy >= self.ty or dy > max_y:
                        # outside vertical bounds for this container/display
                        continue
                    for j, char in enumerate(line):
                        dx = base_x + obj['x'] + j
                        if dx < 0 or dx >= self.tx or dx > max_x:
                            # clip horizontally at container/display edge
                            break
                        self.terminal[dy][dx] = char

        # after rendering, update the terminal
        self.update()
        # save current terminal as last_terminal
        self.last_terminal = [row[:] for row in self.terminal]
        # clear objects
        self.objects = []