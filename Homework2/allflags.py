import flagOne as fone
import flagTwo as ftwo
import flagThree as fthree
import flagFour as ffour

respOne = fone.main()
respTwo = ftwo.main()
respThree = fthree.main()
respFour = ffour.main()


print("===============flags below=================")
print(respOne.split("flag is ")[1].split('"')[0])
print(respTwo.split("flag is ")[1].split('"')[0])
print(respThree.split("flag is ")[1].split('"')[0])
print(respFour.split("flag is ")[1].split('"')[0])