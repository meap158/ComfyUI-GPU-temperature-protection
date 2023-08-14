import subprocess
import sys
import time


class GPUTemperatureProtection:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    last_call_time = time.time()

    def title(self):
        return "GPU temperature protection"

    def process(self):
        if self.enabled == 'True':
            return self.gpu_temperature_protection()
        return

    @staticmethod
    def get_gpu_temperature():
        try:
            return int(subprocess.check_output(
                ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader']).decode().strip())
        except subprocess.CalledProcessError as e:
            print(f"[Error GPU temperature protection]: {e.output.decode('utf-8').strip()}")
        except Exception as e:
            print(f'[Error GPU temperature protection]: {e}')
        return 0

    def gpu_temperature_protection(self):
        # Get the current GPU temperature
        gpu_core_temp = self.get_gpu_temperature()
        print(f'GPU Temperature: {gpu_core_temp}')
        # Check if GPU temperature protection is enabled
        if self.enabled == 'True':
            # Get the current time
            call_time = time.time()
            # Check if the minimum interval has passed since the last call
            if call_time - GPUTemperatureProtection.last_call_time > self.min_interval:
                # Update the GPU temperature again
                gpu_core_temp = self.get_gpu_temperature()
                # Check if the GPU temperature is above the sleep threshold
                if gpu_core_temp > self.sleep_temp:
                    # Check if printing GPU temperature is enabled
                    if self.print_enabled == 'True':
                        print(f'\n\nGPU Temperature: {gpu_core_temp}')
                    # Sleep for a specified time
                    time.sleep(self.sleep_temp)
                    # Update GPU temperature after sleeping
                    gpu_core_temp = self.get_gpu_temperature()
                    # Continue sleeping and checking temperature while conditions are met
                    while (
                        gpu_core_temp > self.wake_temp
                        and (not self.max_sleep_time or self.max_sleep_time > time.time() - call_time)
                        and self.enabled == 'True'
                    ):
                        # Print GPU temperature if printing is enabled
                        if self.print_enabled == 'True':
                            print(f'GPU Temperature: {gpu_core_temp}')
                        # Sleep for a specified time
                        time.sleep(self.sleep_temp)
                        # Update GPU temperature after sleeping
                        gpu_core_temp = self.get_gpu_temperature()
                    # Update the last call time
                    GPUTemperatureProtection.last_call_time = time.time()
                else:
                    # Update the last call time when GPU temperature is below sleep threshold
                    GPUTemperatureProtection.last_call_time = call_time
        # Return the final GPU temperature
        return gpu_core_temp

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                # Enable GPU temperature protection
                "enabled": (["True", "False"],),
                # Print GPU Core temperature while sleeping in terminal
                "print_enabled": (["True", "False"],),
                # GPU temperature monitor minimum interval
                "min_interval": ("INT", {
                    "default": 5,
                    "min": 0,
                    "max": sys.maxsize,
                    "step": 1,
                    "display": "number"
                }),
                # Sleep Time
                "sleep_time": ("INT", {
                    "default": 5,
                    "min": 0,
                    "max": sys.maxsize,
                    "step": 1,
                    "display": "number"
                }),
                # Max sleep time
                "max_sleep_time": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": sys.maxsize,
                    "step": 1,
                    "display": "number"
                }),
                # GPU sleep temperature
                "sleep_temp": ("INT", {
                    "default": 82,
                    "min": 0,
                    "max": 125,
                    "step": 1,
                    "display": "slider"
                }),
                # GPU wake temperature
                "wake_temp": ("INT", {
                    "default": 52,
                    "min": 0,
                    "max": 125,
                    "step": 1,
                    "display": "slider"
                }),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "main"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def main(self, **kwargs):
        self.__dict__.update(kwargs)
        gpu_core_temp = self.process()
        return (gpu_core_temp,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "GPUTemperatureProtection": GPUTemperatureProtection
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "GPUTemperatureProtection": "GPU Temperature Protection"
}
