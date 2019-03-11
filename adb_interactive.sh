#!/bin/bash
version="1.22"
v=0

while [ "$1" != "" ]; do
  case "$1" in
  "-h") echo "
    $0 is a tool to send adb commands to an android device.
    After launching it, use:
      * cursor keys to send adb shell input KEYCODE_DPAD-up,down,right or left
      * DELETE sends a KEYCODE_BACK command
      * DEL sends a KEYCODE_DEL
      * ENTER sends a KEYCODE_ENTER
      * Alphanumeric keys send the corresponding character.
      * Keypad 7: KEYCODE_HOME
      * Keypad 9: KEYCODE_POWER
      * Keypad 1: KEYCODE_MENU
      * Keypad 3: KEYCODE_APP_SWITCH
      * F2 does a swipe up from the bottom of the screen (brings up list of apps on AOSPP)
      * F3 does a swipe down from the top (reveals the quick settings on AOSPP)
      * F5 swipes from middle towards left
      * F6 swipes from middle towards up
      * F7 swipes from middle towards down
      * F8 swipes from middle towards right
      * The character tilde (~) will give you a prompt to enter coordinates to tap on screen
 
    Use with option -s <device serial> to target a specific device.
    Use -v to increase verbosity
    Use ^C to exit
"
        exit 0
        ;;
  "-s") G=$2
        shift
        ;;
  "-v") ((v++))
        echo "Verbosity set to $v"
        ;;
  *)    echo "Unknown option: <$1>"
        ;;
  esac
  shift
done

get_device_id () {
  if [ -z "$G" ]; then
    G=$(adb devices | grep -E "^[0-9A-F]" | cut -f1)
    if [ -z "$G" ]; then echo "No device found"; exit; fi
    if [ $(echo "$G" | wc -l) -gt 1 ]; then
      echo -e "More than 1 device found.\nSelect which one you want to use:"
      select x in $G; do
        G=$x
        break
      done
      fi
    fi
    if [ $(adb devices | grep device | grep -c $G) -eq 0 ]; then
      echo "Is device $G connected? $(adb devices | grep $G)"
      while [ $(adb devices | grep device | grep -c $G) -eq 0 ]; do
      sleep 1; echo -n .
    done
    echo
  fi
}

print_key() {
  if [ $v -gt 0 ]
  then k="$1"
       if [ "$k" == "" ]
       then echo -n "Esc"
       else echo -n "$k"
       fi
  fi
}

get_device_id
echo "$0 version $version"
echo "Using device $G"
size=$(adb -s $G shell wm size | cut -d: -f2)
sizeH=$(echo $size | cut -dx -f1)
sizeV=$(echo $size | cut -dx -f2)
echo "Screen size: $sizeH x $sizeV"

while [ 1 ]; do
   keyevent=UNKNOWN
   IFS="" read -sn1 s
   print_key "$s"
   if [ "$s" == "" ]; then
      read -sn1 t
      print_key "$t"
      if [ "$t" == "[" ]; then
         read -sn1 u
         print_key "$u"
         case ${u} in
         A) keyevent=KEYCODE_DPAD_UP;;
         B) keyevent=KEYCODE_DPAD_DOWN;;
         C) keyevent=KEYCODE_DPAD_RIGHT;;
         D) keyevent=KEYCODE_DPAD_LEFT;;
         1) read -sn1 tilde
            print_key "$tilde"
            case "$tilde" in
            "~") keyevent=KEYCODE_HOME;;      # Keypad 7
              5) keyevent=skip; echo " Swipe left"; 
                 adb -s $G shell input swipe $((sizeH/2)) $((sizeV/2)) 0 $((sizeV/2));;
              7) keyevent=skip; echo " Swipe up"; 
                 adb -s $G shell input swipe $((sizeH/2)) $((sizeV/2)) $((sizeH/2)) 0;;
              8) keyevent=skip; echo " Swipe down"; 
                 adb -s $G shell input swipe $((sizeH/2)) $((sizeV/2)) $((sizeH/2)) $sizeV;;
              9) keyevent=skip; echo " Swipe right"; 
                 adb -s $G shell input swipe $((sizeH/2)) $((sizeV/2)) $sizeH $((sizeV/2));;
              *) if [ $v -eq 0 ]; then echo "unknown: ESC [ $tilde"; fi;;
            esac;;
         H)                 keyevent=KEYCODE_HOME;;      # Keypad 7
         3) read -sn1 tilde;keyevent=KEYCODE_DEL ; print_key "$tilde";;       # DEL key
         4) read -sn1 tilde;keyevent=KEYCODE_MENU; print_key "$tilde";;      # Keypad 1
         F)                 keyevent=KEYCODE_MENU;;      # Keypad 1
         5) read -sn1 tilde;keyevent=KEYCODE_POWER;print_key "$tilde";;     # Keypad 9
         6) read -sn1 tilde;keyevent=KEYCODE_APP_SWITCH;print_key "$tilde";;# Keypad 3
         *) if [ $v -eq 0 ]; then echo "unknown: ESC [ $u"; fi;;
         esac
      elif [ "$t" == "O" ]; then
         read -sn1 u
         print_key "$u"
         keyevent=skip
         case "$u" in
         Q) echo " Swipe UP $((sizeH/2)) $((sizeV-10)) $((sizeH/2)) $((sizeV/2))"
            adb -s $G shell input swipe $((sizeH/2)) $((sizeV-10)) $((sizeH/2)) $((sizeV/2));;
         R) keyevent=skip; echo " Swipe down from top"; 
            adb -s $G shell input swipe $((sizeH/2)) 0 $((sizeH/2)) $((sizeV/2))
            sleep 1
            adb -s $G shell input swipe $((sizeH/2)) 110 $((sizeH/2)) $((sizeV/2))
            ;;
         S) echo " F4 (unassigned)";;
         *) echo " (unassigned)";;
         esac
      else
         if [ $v -eq 0 ]; then echo "ESC+$t ???"; fi
         keyevent=skip
      fi
   elif [ "$s" == "" ]; then
      keyevent=KEYCODE_ENTER
   elif [ "$s" == " " ]; then
      keyevent=KEYCODE_SPACE
   elif [ "$s" == "\t" ]; then
      keyevent=KEYCODE_TAB
   elif [ "$s" == "" ]; then
      keyevent=KEYCODE_BACK
   elif [ "$s" == "	" ]; then
      keyevent=KEYCODE_TAB
   elif [ "$s" == "~" ]; then
      read -p "Enter horizontal and vertical coordinates to tap (ex: 100 200): " x y
      echo "Tapping coordinates <$x> <$y>"
      adb -s $G shell input tap $x $y
      keyevent=skip
   fi
   if [ $keyevent == "UNKNOWN" ]; then
      echo -e " Letter <$s>"
      if [ "$s" == "\"" ]; then s="\\\""; fi
      if [ "$s" == "'"  ]; then s="\\'" ; fi
      adb -s $G shell "input text $s"
   elif [ $keyevent != "skip" ]; then
      echo -e " $keyevent"
      adb -s $G shell input keyevent $keyevent
   fi
done
