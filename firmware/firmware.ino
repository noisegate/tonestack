/* DAP Bass enhance example SGTL5000 only

This example code is in the public domain
*/

#include <Audio.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <SerialFlash.h>


const int myInput = AUDIO_INPUT_LINEIN;
// const int myInput = AUDIO_INPUT_MIC;
const int linelevel[] = {31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13};
const float vpp[] = {1.16,1.22,1.29,1.37,1.44,1.53,1.62,1.71,1.8,1.91,2.02,2.14,2.26,2.39,2.53,2.67,2.83,2.98,3.16};
// Create the Audio components.  These should be created in the
// order data flows, inputs/sources -> processing -> outputs
//

AudioInputI2S       audioInput;         // audio shield: mic or line-in
AudioOutputI2S      audioOutput;        // audio shield: headphones & line-out

// Create Audio connections between the components
//
AudioConnection c1(audioInput, 0, audioOutput, 0); // left passing through
AudioConnection c2(audioInput, 1, audioOutput, 1); // right passing through

// Create an object to control the audio shield.
// 
AudioControlSGTL5000 audioShield;


//fft stuff
//AudioAnalyzeFFT256       fft256_1;       //xy=271,49
//AudioConnection          patchCord1(adc1, fft256_1);

//peak stuff
//AudioAnalyzePeak         peak1;          //xy=352,74
//AudioAnalyzePeak         peak2;          //xy=358,112
//AudioConnection          patchCord1(audioInput, 0, peak1, 0);
//AudioConnection          patchCord2(audioInput, 1, peak2, 0);




void setup() {
  // Audio connections require memory to work.  For more
  // detailed information, see the MemoryAndCpuUsage example
  AudioMemory(4);
  // Enable the audio shield and set the output volume.
  audioShield.enable();
  audioShield.inputSelect(myInput);
  audioShield.volume(0.7);
  // just enable it to use default settings.
  audioShield.audioPostProcessorEnable();
  //audioShield.enhanceBassEnable(); // all we need to do for default bass enhancement settings.
  //audioShield.enhanceBass((float)lr_level,(float)bass_level);
  
  //celloaudioShield.enhanceBass((float)0.5,(float)0.5);
  // audioShield.enhanceBass((float)lr_level,(float)bass_level,(uint8_t)hpf_bypass,(uint8_t)cutoff);
  // please see http://www.pjrc.com/teensy/SGTL5000.pdf page 50 for valid values for BYPASS_HPF and CUTOFF

  audioShield.eqSelect(3);//eq
  audioShield.eqBands(0.0,0.0,0.0,0.0,0.0);
  //audioShield.lineOutLevel(20, 20);
  //audioShield.muteHeadphone();
  audioShield.unmuteLineout();
  //serial comm
  Serial.begin(38400);
  
}

elapsedMillis chgMsec=0;
float lastVol=0.5;
float vol=0.7;
float bass =0.0;
float midbass = 0.0;
float mid =0.0;
float midtreble=0.0;
float treble = 0.0;
float left = 0.0;
float right = 0.0;

float diff;
float sign;
int inByte;
int step;
int level=2;//default 
float peakval=0.0;

void reduce(float *parameter)
{
    //prevent plops, slowly reduce in 0.04 steps
    if (*parameter<0) sign = -1.0;
    else sign = 1.0;
  
    step = (int)abs(*parameter/0.04);

    for (int i=0; i<step;i++) {
      
      *parameter = *parameter - sign*0.04;
      audioShield.eqBands(bass, midbass, mid, midtreble, treble);
      delay(10);
    }
  
}

void defeat(){
  if (bass!=0.0) reduce(&bass);
  if (treble!=0.0) reduce(&treble);
  if (midbass!=0.0) reduce(&midbass);
  if (midtreble!=0.0) reduce(&midtreble);
  if (mid!=0.0) reduce(&mid);
}

void loop() {
  // every 10 ms, check for adjustment
  if (chgMsec > 50) { // more regular updates for actual changes seems better.
    
    float vol1=analogRead(15)/1023.0;
  
    if (Serial.available()>0){
      inByte = Serial.read();
      if (inByte=='d'){
        defeat();
       }
      if (inByte=='D'){
        defeat();
        audioShield.audioProcessorDisable();
      }
      if (inByte=='e'){
        defeat();
        audioShield.audioPostProcessorEnable();
      }
      if (inByte == 'B'){
        bass += 0.04;
      }
      if (inByte == 'b'){
        bass -= 0.04;
      }
      if (inByte == 'N'){
        midbass += 0.04;
      }
      if (inByte == 'n'){
        midbass -= 0.04;
      }

      if (inByte == 'M'){
        mid += 0.04;
      }
      if (inByte == 'm'){
        mid -= 0.04;
      }
      if (inByte == 'Y'){
        midtreble += 0.04;
      }
      if (inByte == 'y'){
        midtreble -= 0.04;
      }

      if (inByte == 'T'){
        treble += 0.04;
      }
      if (inByte == 't'){
        treble -= 0.04;
      }
      if (inByte == 'V'){
        vol += 0.04;
      }
      if (inByte == 'v'){
        vol -= 0.04;
      }

      if (inByte == 'L'){
        level++;
        if (level>18) level=18;
        
        audioShield.lineOutLevel(linelevel[level]);
      }

      if (inByte == 'l'){
        level--;
        if (level<0) level=0;
        
        audioShield.lineOutLevel(linelevel[level]);
      }

      audioShield.eqBands(bass, midbass, mid, midtreble, treble);
      audioShield.volume(vol);

      /*
      if (peak1.available()){
        peakval = peak1.read();
      }
      */
      
      //Serial.print("Tone settings Bass: ");
      Serial.print(bass);
      Serial.print(":");
      Serial.print(midbass);
      Serial.print(":");
      Serial.print(mid);
      Serial.print(":");
      Serial.print(midtreble);
      Serial.print(":");
      Serial.print(treble);
      Serial.print(":");
      Serial.print(right-left);
      Serial.print(":");
      Serial.print(vol);
      Serial.print(":");
      Serial.print(vpp[level]);
      Serial.print(":");
      Serial.println(peakval);

    }

    /*
    if (mode == 1){
    
    if((vol1 - lastVol)>0.04){
      
      //audioShield.volume(vol1);
      bass += 0.04;//0.5 dB
      lastVol+=0.04;
      if (bass>1.0) bass=1.0;
      //lastVol=vol1;
      audioShield.eqBands(bass,treble);
      Serial.print("Bass increment ");
      Serial.println(bass);
    }
    if((lastVol-vol1)>0.04){
      
      //audioShield.volume(vol1);
      bass -= 0.04;//0.5 dB
      lastVol-=0.04;
      if (bass<0.0) bass=0.0;
      //lastVol=vol1;
      audioShield.eqBands(bass,treble);
      Serial.print("Bass decrement ");
      Serial.println(bass);

    }
    */
    chgMsec = 0;
    
    //audioShield.volume(0.7);
  }
}

