# notatka do klienta

## stan klienta - w trakcie

	refactor, ulepszenie, poprawa czytelnosci kodu

## Dane:
	Przykładowy adres w sieci Bitcoin (prod) zawierający kilka OP_RETURN - do testów
	```bash
	address -> 1PdNVV71qNbHxchKiRrxqoR8JohpaLfoMX
	```

	Dane do testów drzewa merkle: 
	```python
		child: a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
		child: 5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5
		child: ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f
		child: asdfasdfasdfasdfasdfasdfa5d3f8c7623048c9c063d532cc95c5edasdasdad
		child: hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni

		get_proof: hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni
		verify_proof:
			item: hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni
			proof: [['up', 'hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni'], ['up', 'hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni'], ['right', '6de4c2ebc51eef4be83edb4b91ef95ba395858ee398b5301339d8174ede3a9ed']]
	```
	Binarka:
	```python
		rufus.exe -- jakis tam program do formatowania usb
		podpisana komenda: osslsigncode  sign -h sha2 -certs certyfikat.crt -key klucz.key -n '1PdNVV71qNbHxchKiRrxqoR8JohpaLfoMX' -i 'http://google.pl' -in rufus-3.13.exe -out podpisana-binarka.exe -verbose 
	```
