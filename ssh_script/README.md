
## login script
 this scripts is used for login to server what has been installed `expect` . if you don't get this package ,you can
```
brew install expect 
```
on macOs or 
```
apt-get install expect
```
on Ubuntu. after install you can 
```
expect -v
``` 
to check it's works or not
 
### how use 

 download the shell scripts and the `.exp` scripts . move them to  a safety  place , then

- open locate.sh and change the default params.so that you can use it without any params .`tips: host can print like '192.168.*.'  `
- you can link it on your bash shell or zsh shell .

here is my configuration on zsh

```
rmt () { cd /path/to/location/ && sh locate.sh $*;}
```
and source you `.zshrc` file. now you can use `rmt` keyword  to login  server automatically .

you can manager the `.exp` scripts  to do anything after has Logged to a server. 

have fun.([or you may want to download living videos, you can follow this project](https://github.com/fulln/sampleScrips))
 
<a href="../README.md">&lt;——Back to Menus</a> 
