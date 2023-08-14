# GPU temperature protection
### Pause image generation when GPU temperature exceeds threshold
this extension uses nvidia-smi to monitor GPU temperature at the end of each step, if temperature exceeds threshold pause image generation until criteria are met.

## Requirements
Nvidia GPU

## Installation
- To install this custom node for ComfyUI, clone the repository using Git or download it, and then copy the node files to: ComfyUI\custom_nodes\ComfyUI-GPU-temperature-protection
```
https://github.com/meap158/ComfyUI-GPU-temperature-protection.git
```

## Setting

- `GPU temperature monitor minimum interval`
    - checking temperature too often will reduce image generation performance
    - set to `0` well effectively disable this extension
    - to completely disable extension disable the file extension tab
- `GPU sleep temperature`
    - generation will pause if GPU core temperature exceeds this temperature
- `GPU wake temperature`
    - generation will continue to pause until temperature has drops below this temperature 
    - setting a higher value than `GPU sleep temperature`will effectively disable this
- `Sleep Time`
    - seconds to sleep before checking temperature again
- `Max sleep Time` 
    - max number of seconds that it's allowed to pause
    - generation will continue disregarding `GPU wake temperature` after the allotted time has passed
    - set to `0` disable this limit allowing it to pause indefinitely
- `Print GPU Core temperature while sleeping in terminal`
    - print the GPU core temperature reading from nvidia-smi to console when generation is paused
    - providing information

## Usage
To use the custom node, simply connect it to a node with the output being an image, such as VAE Decode as shown in the screenshot below:

## Notes
- Temperature unit Celsius, Time unit seconds
- To be honest I don't recommend anyone using this extension, if your GPU is having temperature issues and don't have the means to improve the cooling, then recommend using software like MSI afterburner to undervolt or further power limit or thermal limit the GPU.
