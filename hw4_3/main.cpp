#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"

Ticker servo_ticker;
PwmOut pin5(D5), pin6(D6);
BBCar car(pin5, pin6, servo_ticker);

// BufferedSerial pc(USBTX,USBRX); //tx,rx
BufferedSerial uart(D1,D0); //tx,rx

int main() {
   char buf[256], outbuf[256];
   FILE *devin = fdopen(&uart, "r");
   FILE *devout = fdopen(&uart, "w");
   uart.set_baud(9600);

   while (1) {
      memset(buf, 0, 256);
      for( int i = 0; ; i++ ) {
         char recv = fgetc(devin);
         if(recv == '\n') {
            printf("\r\n");
            break;
         }
         buf[i] = fputc(recv, devout);
      }
   RPC::call(buf, outbuf);
   }
}


// #include"mbed.h"
// #include "bbcar.h"

// Ticker servo_ticker;
// PwmOut pin5(D5), pin6(D6);
// BBCar car(pin5, pin6, servo_ticker);

// BufferedSerial pc(USBTX,USBRX); //tx,rx
// BufferedSerial uart(D1,D0); //tx,rx

// int main(){
//     double angle = 0;
//     double int_temp = 0, dec_temp = 0;
//     bool is_int = true;
//     int dec_ind = 1;
//     uart.set_baud(9600);
   
//     while(1){
//         if(uart.readable()){
//             char recv[1];
//             uart.read(recv, sizeof(recv));
//             // pc.write(recv, sizeof(recv));

//             if (recv >= '0' && recv <= '9'){
//                 if (is_int){
//                     int_temp *= 10;
//                     int_temp += double(int(recv - '0'));
//                 }
//                 else {
//                     dec_temp += double(int(recv - '0')) / (10 * dec_ind++);
//                 }
//             }
//             else if (recv = '.') {
//                 is_int = false;
//             }
//             else {
//                 break;
//             }
//         }
//     }
    
// }