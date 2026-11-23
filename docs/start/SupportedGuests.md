<!-- order: 3 -->
# Supported Guests
## macOS

<img align="left" width="90" height="90" src="../images/7b9b72ee.png">

<img align="left" src="../images/8f69f9b9.png" height=900 width=2 />

<h3>macOS Sequoia<br></h3>

This project currently supports the latest version of macOS Sequoia, as well as every prior version down to macOS High Sierra. 

The option to use legacy versions is available, but no support will be provided and any issues you encounter are your own to solve!<br>

### Supported

<h5><img align="middle" width="35" height="35" src="../images/aa49b5ba.png"> macOS Sonoma</h5>
<h5><img align="middle" width="35" height="35" src="../images/4829ebb4.png"> macOS Ventura</h5>
<h5><img align="middle" width="35" height="35" src="../images/7d341cce.png"> macOS Monterey</h5>
<h5><img align="middle" width="35" height="35" src="../images/79a7a051.png"> macOS Big Sur</h5>
<h5><img align="middle" width="35" height="35" src="../images/cd8029e8.png"> macOS Catalina</h5>
<h5><img align="middle" width="35" height="35" src="../images/184bb2ef.png"> macOS Mojave</h5>
<h5><img align="middle" width="35" height="35" src="../images/bd4a791d.png"> macOS High Sierra</h5><br>


### Legacy

<h5><img align="middle" width="35" height="35" src="../images/788860d8.png"> macOS Sierra</h5>
<h5><img align="middle" width="35" height="35" src="../images/bbec9fdd.png"> Mac OS X El Capitan</h5>
<h5><img align="middle" width="35" height="35" src="../images/9ddac84f.png"> Mac OS X Yosemite</h5>
<h5><img align="middle" width="35" height="35" src="../images/08ec7706.png"> Mac OS X Mavericks</h5>
<h5><img align="middle" width="35" height="35" src="../images/a99666cf.png"> Mac OS X Mountain Lion</h5>
<h5><img align="middle" width="35" height="35" src="../images/03719dd8.png"> Mac OS X Lion</h5>

<!-- <h5><img align="middle" width="35" height="35" src="https://static.wikia.nocookie.net/ipod/images/e/e4/Mac_OS.png/revision/latest?cb=20100820010621"> Mac OS 9</h5> --> 
<!-- Teehee -->


<br>
<br>

## Feature Table


This table is a very **loose** representation of the current state of macOS versions and their support with ULTMOS / QEMU / KVM. It's more for reference and shouldn't be taken seriously.

If you find something is wrongly marked, please feel free to update it.

<br>

|                          	| <img align="center" width="35" height="35" src="../images/bd4a791d.png"> | <img align="center" width="35" height="35" src="../images/184bb2ef.png">     	| <img align="center" width="35" height="35" src="../images/cd8029e8.png">     	| <img align="center" width="35" height="35" src="../images/79a7a051.png">     	| <img align="center" width="35" height="35" src="../images/7d341cce.png">     	| <img align="center" width="35" height="35" src="../images/4829ebb4.png">     	| <img align="center" width="35" height="35" src="../images/aa49b5ba.png">      	| <img align="center" width="35" height="35" src="../images/7b9b72ee.png">      	|
|--------------------------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:---------:|:---------:|
|            **AutoPilot** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|
|     **Auto<br>Download** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|
|    **Online<br>Install** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|
|   **Offline<br>Install** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|
|       **QEMU<br>Script** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓¹   	|    ✓¹    	|    ✓¹    	|
|      **Virt<br>Manager** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ?²  	|    ?²   	|    ?²   	|
|   **GPU<br>Passthrough** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓¹   	|    ✓¹    	|    ✓¹    	|
| **VirtIO<br>Networking** 	|    ✕   	|    ✕   	|    ?³   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|
| **VirtIO<br>Storage** 	|    ✕   	|    ✕   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|


¹ <sup>If trying to boot macOS Ventura and later with GPU passthrough, you may need to do so using Virtual Machine Manager. The QEMU script may have issues with GPU passthrough.<sup>

² <sup>macOS Ventura and later have been known to have issues booting    *without* GPU passthrough in Virtual Machine Manager.</sup>

³ <sup>I have no idea whether or not VirtIO networking works on macOS Catalina.</sup>

