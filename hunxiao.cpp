#include <iostream>
#include <string>
// logic
#define rg if
#define fz else
#define equ ==
#define neq !=
#define lss <
#define gtr >
// begin end
#define b {
#define e }
#define rh ;
// using namespace
#define sy using
#define mmgs namespace
// loop
#define cf for
#define d while
#define tcxh break
#define jx continue
// iostream
/* flish (lxxs): ensures the output (cout/sc)is immediately sent to the console:
             #include <iostream>
             #include <string>
             #include <thread>
             #include <chrono>
             int main() {
                 const string clear_current_line = "\33[2K\r";
                 for (int i = 0; i < 5; ++i) {
                     std::cout << clear_current_line << "Processing item " << i+1 << flush;
                     std::this_thread::sleep_for(std::chrono::milliseconds(500)); // time.sleep(0.500)
                 }
                 std::cout << std::endl; // \n after the progress (ignore if no need \n)
                 std::cout << "FInished processing." << std::endl; // finished message (can be ignored)
                 return 0;
             }
*/
#define sr cin
#define sc cout
#define lxxs flush
#define al <<
#define ar >>
#define gh endl
// function
#define zhs main
#define ks class
#define xk void
#define db struct
#define bgk private
#define gk public
#define fh return
// value type / variable
#define ro const
#define zs int
#define fds float
#define ss double
#define wz std::string
#define ygz char
// unsigned signed int
#define wqm unsigned
#define qm signed
#define zs8 int8_t
#define zs16 int16_t
#define zs32 int32_t
#define zs64 int64_t
#define zs8u uint8_t
#define zs16u uint16_t
#define zs32u uint32_t
#define zs64u uint64_t
// switch
#define lg switch
#define sj case
#define mr default
// -------------------------------------

xk 

sy mmkj std;
zs zhs() {
    sc al "Hello, World!" al gh;
    fh 0;
}
