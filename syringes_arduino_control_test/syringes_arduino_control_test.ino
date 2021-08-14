//Possible to-do
//Add a stopper for the max step - however we dont need that much of pressure at this stage.

//#include <arduino-timer.h>

//auto timer = timer_create_default();

#define STEPS_PER_REVOLUTION 200*16
#define ISR_FREQ 25000
#define MAX_MOTOR_SPEED_STEPS 25000 // 25000 Steps/s
#define MAX_MOTOR_SPEED 10000
#define MAX_MOTOR_TICKS 1000000;
#define SPEED2TICKS(target_speed)((unsigned int)((float)ISR_FREQ/target_speed))
#define INVERT_DIRECTION false
#define FORWARD (!INVERT_DIRECTION ? HIGH : LOW)
#define BACKWARD (!FORWARD)

//#define PRESSURE_SENSORS ADP5101 42.1316
//#define PRESSURE_SENSORS ADP51A11 10.0683
#define PRESSURE_SENSORS ADP5100 51.8323
#define PRESSURE_FROM_RAW(value)((float)value*0.00488*51.8323)
//#define PRESSURE_FROM_RAW(value)((float)value*0.00488*10.0683) // TODO: put sensor calibration



#define INIT_COMMUNICATION 1
#define STOP_CMD 255
#define RESTART_CMD 254
#define HOME 253
#define SET_CMD 2
#define TARGET_PRESSURE_1 111
#define TARGET_PRESSURE_2 112
#define TARGET_PRESSURE_3 113
#define TARGET_PRESSURE_4 114
#define TARGET_PRESSURE_5 115
#define TARGET_PRESSURE_6 116
#define TARGET_PRESSURE_7 117
#define TARGET_PRESSURE_8 118
#define TARGET_PRESSURE_9 119
#define PID_GAINS 12


const unsigned int n_motors = 3;
//unsigned long cnt[n_motors];
//unsigned long mtr_ticks[n_motors];
unsigned long cnt[n_motors];
unsigned long mtr_ticks[n_motors];

bool motor_enabled[n_motors];

int home_counter = 0;
float offset_p[n_motors]; // offset pressure
float p_d[n_motors]; // target pressure
float p[n_motors]; // pressure

float sp[n_motors] = {0.0, 0.0, 0.0}; // smoothed pressure
float steps[n_motors] = {0.0, 0.0, 0.0};
float e[n_motors] = {0.0, 0.0, 0.0};
float eI[n_motors] = {0.0, 0.0, 0.0};
float e_prev[n_motors] = {0.0, 0.0, 0.0};
float u[n_motors] = {0.0, 0.0, 0.0};
float kp[n_motors] = {2000.0, 2000.0, 2000.0};
float ki[n_motors] = {100.0, 100.0, 100.0};
float kd[n_motors] = {0.0, 0.0, 0.0};

//float sp[n_motors] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
//float steps[n_motors] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
//float e[n_motors] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
//float eI[n_motors] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
//float e_prev[n_motors] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
//float u[n_motors] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
//float kp[n_motors] = {2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0};
//float ki[n_motors] = {100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0};
////float ki[n_motors] = {0.0, 0.0, 0.0};
//float kd[n_motors] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
const float ss_percentage = 5 / 100;
const float dt = 1.0 / 100.0; // Must match the Timer 2 frequency

//Pins
//const int stepPins[n_motors] = {2, 4, 6};
//const int dirPins[n_motors] = {3, 5, 7};
//const int analogPins[n_motors] = {A0, A1, A2};
//const int valvePin = 50;
//const int buttonPins[n_motors] = {30, 32, 34};

//TOP
const int stepPins[n_motors] = {19, 2, 8};
const int dirPins[n_motors] = {16, 5, 11};
const int buttonPins[n_motors] = {44, 50, A13};
const int analogPins[n_motors] = {A6, A3, A0};
const int valvePins[n_motors] = {26, 32, 38};

//MIDDLE
//const int stepPins[n_motors] = {18,3,9};
//const int dirPins[n_motors] = {15,6,12};
//const int buttonPins[n_motors] = {42, 48, A14};
//const int analogPins[n_motors] = {A7, A4, A1};
//const int valvePins[n_motors] = {24,30,36};

//BOTTOM
//const int stepPins[n_motors] = {17, 4, 10};
//const int dirPins[n_motors] = {14, 7, 13};
//const int buttonPins[n_motors] = {40, 46, A15};
//const int analogPins[n_motors] = {A8, A5, A2};
//const int valvePins[n_motors] = {22, 28, 34};

//Breadboard
//const int stepPins[n_motors] = {12, 10, 8};
//const int dirPins[n_motors] = {13, 11, 9};
//const int buttonPins[n_motors] = {2, 3, 4};
//const int analogPins[n_motors] = {A13, A14, A15};
//const int valvePins[n_motors] = {24, 24, 24};

//full pcb
//const int stepPins[n_motors] = {19, 2, 8, 18, 3, 9, 17, 4, 10};
//const int dirPins[n_motors] = {16, 5, 11, 15, 6, 12, 14, 7, 13};
//const int buttonPins[n_motors] = {44, 50, A13, 42, 48, A14, 40, 46, A15};
//const int analogPins[n_motors] = {A6, A3, A0, A7, A4, A1, A8, A5, A2};
//const int valvePins[n_motors] = {26, 32, 38, 24, 30, 36, 22, 28, 34};

bool steady_state = false;

bool stop_control_system = true;

bool gohome[n_motors] = {false, false, false};
bool stopnow = true;

String message, out, output;

void setup()
{
  // Stop interrupts
  cli();

  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  //OCR1A = 15624;// = (16*10^6) / (1*1024) - 1 (must be <65536) // 1hz increments with 1024 prescaler
  OCR1A = 9; // = (16*10^6) / (25000*64) - 1 (must be <65536) // 25 Khz increments with 64 prescaler
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  //TCCR1B |= (1 << CS12) | (1 << CS10);  // Set CS12 and CS10 bits for 1024 prescaler
  TCCR1B |= (1 << CS01) | (1 << CS00); // This should be the 64 prescaler
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);

  TCCR2A = 0;// set entire TCCR2A register to 0
  TCCR2B = 0;// same for TCCR2B
  TCNT2  = 0;//initialize counter value to 0
  // set compare match register for 100hz increments
  OCR2A = 156;// = (16*10^6) / (100*1025) - 1 (must be < 256)
  // turn on CTC mode
  TCCR2A |= (1 << WGM21);
  // Set CS21 bit for 1024 prescaler
  TCCR2B |= (1 << CS12) | (1 << CS10);
  // enable timer compare interrupt
  TIMSK2 |= (1 << OCIE2A);



  //  timer.every(1000, print_message);

  for (int i = 0; i < n_motors; i++)
  {
    pinMode(stepPins[i], OUTPUT);
    pinMode(dirPins[i], OUTPUT);
    pinMode(buttonPins[i], INPUT);
    pinMode(valvePins[i], OUTPUT);

    cnt[i] = 0;
    mtr_ticks[i] = 10000;
    motor_enabled[i] = true;
    //p_d[i] = p[i]; // set error equal to zero ad the beginning
    //e[i] = e_prev[i] = p_d[i] - p[i];
    e[i] = e_prev[i] = 0;
    delay(10);
  }

  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  Serial.setTimeout(1);

  // get offset
  for (int i = 0; i < n_motors; i++) {
    offset_p[i] = analogRead(analogPins[i]) * 0.0048828125 * 51.8323; //measure offset
    //delay(1);
  }

  for (int i = 0; i < n_motors; i++)
  {
    // TODO: use port manipulation
    digitalWrite(dirPins[i], LOW);
  }

  for (int i = 0; i < n_motors; i++) {
    digitalWrite(valvePins[i], LOW);
  }

  // Enable interrupts
  sei();
}

ISR(TIMER1_COMPA_vect)
{

  //  if (gohome) {
  //    for (int i = 0; i < n_motors; i++)
  //    {
  //      steps[i] = 0;
  //    }
  //  }

  if (stop_control_system)
  {
    for (int i = 0; i < n_motors; i++)
    {
      eI[i] = 0;
      cnt[i] = 0;
    }
  }

  else {
    for (int i = 0; i < n_motors; i++)
    {
      cnt[i]++;
      //Serial.println("hi");

      if (cnt[i] >= mtr_ticks[i])
      {

        //Serial.println(mtr_ticks[0]);
        // TODO: use port manipulation
        cnt[i] = 0;
        if (motor_enabled[i]) {
          //Serial.println("hi");
          digitalWrite(stepPins[i], HIGH);
          //delayMicroseconds(20);
          digitalWrite(stepPins[i], LOW);
          //        if (digitalRead(dirPins[i] == FORWARD)) {
          //          steps[i] = steps[i] + 1;
          //        }
          //        else {
          //          steps[i] = steps[i] - 1;
          //        }
        }
      }
    }
  }

}


ISR(TIMER2_COMPA_vect)
{

  //  for (int i = 0; i < n_motors; i++) {
  //    if(digitalRead(buttonPins[i]) == 0){
  //      home_counter
  //    }
  //  }
  if (home_counter == n_motors) {
    for (int i = 0; i < n_motors; i++) {
      digitalWrite(valvePins[i], LOW);
    }
  }

  if (stopnow) {
    stop_control_system = true;
    for (int i = 0; i < n_motors; i++) {
      gohome[i] = false;
    }
    for (int i = 0; i < n_motors; i++) {
      digitalWrite(valvePins[i], LOW);
    }

  }
  else {
    stop_control_system = false;
    for (int i = 0; i < n_motors; i++)
    {
      //Home check
      if (gohome[i] == true && digitalRead(buttonPins[i]) == 1) {
        for (int i = 0; i < n_motors; i++) {
          digitalWrite(valvePins[i], HIGH);
        }
        digitalWrite(dirPins[i], BACKWARD);
        mtr_ticks[i] = SPEED2TICKS((unsigned int)abs(10000));
        //Serial.println("valve is on");
        motor_enabled[i] = true;
        p_d[i] = 0;
        p[i] = 0;
        sp[i] = 0;
        eI[i] = 0;
      }
      else if (gohome[i] == true && digitalRead(buttonPins[i]) == 0) {
        motor_enabled[i] = false;
        p_d[i] = 0;
        p[i] = 0;
        sp[i] = 0;
        eI[i] = 0;
        gohome[i] = false;
        home_counter++;
      }
      else {
        // PID
        // REMARK: put (eventually) analog read here
        e[i] = (p_d[i] - sp[i]);
        //Serial.println(e[0]);
        if (e[i] > 0) {
          digitalWrite(dirPins[i], FORWARD);
          //Serial.println("Forward");
        }
        else {
          digitalWrite(dirPins[i], BACKWARD);
          //Serial.println("Backward");
        }
        eI[i] += e[i] * dt;
        u[i] =
          kp[i] * e[i] // Proportional
          + ki[i] * eI[i] // Integral
          + kd[i] * (e[i] - e_prev[i]) / dt // Derivative TODO: consider to derive p instead of e to avoid spikes in case of sharp transition in the setpoint
          ;
        //if( p_d[i] -  p_d[i]*ss_percentage < p[i] && p[i] > p_d[i] + p_d[i]*ss_percentage )
        if (abs(e[i]) <= 0.25)
        {
          steady_state = true;
          eI[i] = 0;
          mtr_ticks[i] = MAX_MOTOR_TICKS;
          motor_enabled[i] = false;
        }
        else
        {
          steady_state = false;
          if (abs(u[i]) > MAX_MOTOR_SPEED) {
            u[i] = MAX_MOTOR_SPEED;
          }
          mtr_ticks[i] = SPEED2TICKS((unsigned int)abs(u[i]));

          if (digitalRead(dirPins[i]) == BACKWARD && digitalRead(buttonPins[i]) == 0) {

            motor_enabled[i] = false;
            //Serial.println("Emergency");
          }
          else {
            motor_enabled[i] = true;
          }

          //Safety stop

        }
      }
    }
  }
}

void loop()
{

  // REMARK: Analog read is extremely slow and it mess with the motor command
  //   if put in the ISR2. The resulting command produces higher noise from the stepper.
  // Leave it here for the moment.

  for (int i = 0; i < n_motors; i++) {
    p[i] = analogRead(analogPins[i]) * 0.0048828125 * 51.8323 - offset_p[i];
    sp[i] = 0.9 * p[i] + 0.1 * sp[i];
  }
  //  ////////////////////
  //
  //  //p[1] = p[0]; // TODO: Remove

  if (Serial.available() > 0) {
    message = Serial.readStringUntil(';');
    //delay(1);
  }
  //Serial.println(message);

  switch (message.toInt())
  {
    case STOP_CMD:
      stop_control_system = true;
      stopnow = true;
      break;
    case RESTART_CMD:
      stop_control_system = false;
      for (int i = 0; i < n_motors; i++) {
        gohome[i] = false;
      }
      stopnow = false;
      break;
    case TARGET_PRESSURE_1:
      stopnow = false;
      message = Serial.readStringUntil(';');
      //Serial.print("Setting Target Pressure to: ");
      //Serial.println(message.toFloat());
      p_d[0] = message.toFloat();
      motor_enabled[0] = true;
      stop_control_system = false;
      for (int i = 0; i < n_motors; i++) {
        gohome[i] = false;
      }
      /////
      return;
    case TARGET_PRESSURE_2:
      stopnow = false;
      message = Serial.readStringUntil(';');
      //Serial.print("Setting Target Pressure to: ");
      //Serial.println(message.toFloat());
      p_d[1] = message.toFloat();
      motor_enabled[1] = true;
      stop_control_system = false;
      for (int i = 0; i < n_motors; i++) {
        gohome[i] = false;
      }

      /////
      return;
    case TARGET_PRESSURE_3:
      stopnow = false;
      message = Serial.readStringUntil(';');
      //Serial.print("Setting Target Pressure to: ");
      //Serial.println(message.toFloat());
      p_d[2] = message.toFloat();
      motor_enabled[2] = true;
      stop_control_system = false;
      for (int i = 0; i < n_motors; i++) {
        gohome[i] = false;
      }

      /////
      return;
    case HOME:
      stopnow = false;
      stop_control_system = false;
      home_counter = 0;
      for (int i = 0; i < n_motors; i++) {
        gohome[i] = true;
      }
      break;
    default:
      break;
  }



  output = "";

  for (int i = 0; i < n_motors; i++) {
    output = output + p[i];
    if (i < n_motors - 1) {
      output = output + ",";
    }
    else {
      output = output + ",";
    }

  }

  Serial.println(output);

  delay(200);


  //timer.tick(); // tick the timer

}

//bool print_message(void *) {
//  //Serial.print("print_message: Called at: ");
//  int offsetValvue = offset_p[0] / 0.0048828125 / 10.0683;
//  //  Serial.print(String(offsetValvue) + "%");
//  //  Serial.print(String(analogRead(A3)) + "?");
//  //  Serial.print(String(analogRead(A4)) + "!");
//  //  Serial.print(String(analogRead(A5)) + "!");
//  //  Serial.print(String(message)+"*");
//  return true; // repeat? true
//}

void split_string(String s, float out[])
{
  ;
}
