#Kilka pomysłów jak to zrobic w Windowsie:
## Frida
## AppLocker
		tutaj ta funkcjonalność całkiem dobrze pasuje, ale na ten moment wiadomo tylko, że AppLocker zapewnia rulki
## Monitoring rejestrów - podczas instalowania każdy program coś wpisuje do rejestrów
## Info od kogos
		https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/filter-manager-concepts -- system (minitfilter) driver
		https://github.com/microsoft/Detours - API hooking od CreateFile() calls
## Dołącznie do pliku setup.exe / plików msi "Custom Actions" i tam skrypt
			nie rozwiązuje to problemu pierwszej instalacji