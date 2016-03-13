//adapted version of the nrf24_reliable_datagram_client-pde
//from RadioHead library

#include <RHReliableDatagram.h>
#include <RH_NRF24.h>
#include <SPI.h>
#define CLIENT_ADDRESS 1
#define SERVER_ADDRESS 2
// Singleton in stance of the radio driver
RH_NRF24 driver;
// RH_NRF24 driver(8, 7);   // For RFM73 on Anarduino Mini
// Class to manage message delivery and receipt, using the driver declared above
RHReliableDatagram manager(driver, CLIENT_ADDRESS);
void setup() 
{

  Serial.println("Setting up RF manager...");
  Serial.begin(9600);
  if (!manager.init())
    Serial.println("init failed");
  // Defaults after init are 2.402 GHz (channel 2), 2Mbps, 0dBm
  Serial.println("Registering to master...");
 //Send my id to master to make sure he know I am connected
 //Wait for an OK before entering the loop
  //TODO 
  
}
uint8_t data[] = "Hello from 1";
// Dont put this on the stack:
uint8_t buf[RH_NRF24_MAX_MESSAGE_LEN];
void loop()
{
  Serial.println("Sending to nrf24_reliable_datagram_server");
    
  //Sleepy slave
  //Send a command request to the master
  //0 means go back to sleep
  //n means activate the pump for n seconds
  //delay(300000) sleep 5 minutes

  //Active slave
  //Listen for a command from the master
  //0 means go back to sleep
  //n means activate the pump for n seconds
  //back to lister

// Server example code
  if (manager.available())
  {
    // Wait for a message addressed to us from the master
    uint8_t len = sizeof(buf);
    uint8_t from;
    if (manager.recvfromAck(buf, &len, &from))
    {
      Serial.print("got request from : 0x");
      Serial.print(from, HEX);
      Serial.print(": ");
      Serial.println((char*)buf);

      // Send a reply back to the originator client
      if (!manager.sendtoWait(data, sizeof(data), from))
        Serial.println("sendtoWait failed");
    }
  }
}


/* client example code
  // Send a message to manager_server
  if (manager.sendtoWait(data, sizeof(data), SERVER_ADDRESS))
  {
    // Now wait for a reply from the server
    uint8_t len = sizeof(buf);
    uint8_t from;   
    if (manager.recvfromAckTimeout(buf, &len, 2000, &from))
    {
      Serial.print("got reply from : 0x");
      Serial.print(from, HEX);
      Serial.print(": ");
      Serial.println((char*)buf);
    }
    else
    {
      Serial.println("No reply, is nrf24_reliable_datagram_server running?");
    }
  }
  else
    Serial.println("sendtoWait failed");
  delay(500);
}
*/


