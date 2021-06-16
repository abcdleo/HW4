#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"

Ticker servo_ticker;
PwmOut pin5(D5), pin6(D6);
BufferedSerial xbee(D1, D0);

BBCar car(pin5, pin6, servo_ticker);

int main() {
    
   char buf[256], outbuf[256];
   FILE *devin = fdopen(&xbee, "r");
   FILE *devout = fdopen(&xbee, "w");
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





// #include "mbed.h"
// #include "bbcar.h"
// #include "bbcar_rpc.h"

// Ticker servo_ticker;
// PwmOut pin5(D5), pin6(D6);
// BufferedSerial xbee(D1, D0);

// BBCar car(pin5, pin6, servo_ticker);

// int main() {
//     char buf[256], outbuf[256];
//     FILE *devin = fdopen(&xbee, "r");
//     FILE *devout = fdopen(&xbee, "w");
//     memset(buf, 0, 256);
//     int d_1 = 0, d_2 = 0, dir = 0;

    // for (int i = 0; ; i++) {
    //     char recv = fgetc(devin);
    //     if(recv == '\n') {
    //         printf("\r\n");
    //         buf[i] = fputc(recv, devout);
    //         break;
    //     }
    //     buf[i] = fputc(recv, devout);
    // }

    // for (int i = 0, data_ind = 0; ; i++){
    //     if (buf[i] != ' ') {
    //         if (data_ind == 0){
    //             d_1 *= 10;
    //             d_1 += int(buf[i] - '0');
    //         }
    //         else if (data_ind == 0){
    //             d_2 *= 10;
    //             d_2 += int(buf[i] - '0');
    //         }
    //         else {
    //             if (buf[i] == 'e')  // east
    //                 dir = 1;
    //             else if (buf[i] == 'w') // west
    //                 dir = 2;
    //             else if (buf[i] == 's') // south
    //                 dir = 3;
    //             else if (buf[i] == 'n') // north
    //                 dir = 4;
    //             else 
    //                 printf("ERROR!");
    //             break;
    //         }
    //     }
    //     else
    //         data_ind++;
    // }
    // printf("d_1 = %d, d_2 = %d, dir = %d\n", d_1, d_2, dir);
// }