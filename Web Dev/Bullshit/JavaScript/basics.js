// var firstName = prompt("What is your first name?");
// var lastName = prompt("What is your last name?");
// var age = prompt("What is your age?");
// console.log("Your full name is " + firstName + " " + lastName);
// console.log("Your are " + age + " years old");

// if(age%2 == '1'){
// 	alert("You have an odd age !!");
// 	if(age == '21'){
// 		alert("Wish you a very Happy Birthday !! You are eligible for a free shot");
// 	}
// }
// else if(age < '0') {
// 	alert("You have entered an incorrect age you peice of shit !!");
// }

// var sqaureage = Math.sqrt(age)
// if (sqaureage%1 == '0') {
// 	alert("Bhosadiwaale chacha perfect square");
// }



var numone = -9;
console.log("Print all numbers between -10 and 19")
while(numone < 19){
	console.log(numone);
	numone++;
}

var numtwo = 10;
console.log("Print all even numbers between 10 and 40")
while(numtwo <= 40){
	if(numtwo%2 == 0){
		console.log(numtwo);
	}
	numtwo++;
}

var numthree = 300;
console.log("Print all odd numbers between 300 and 333")
while(numthree <= 333){
	if(numthree%2 != 0){
		console.log(numthree);
	}
	numthree++;
}

var numfour = 5;
console.log("Print all numbers divisible by 5 and 3 between 5 and 50")
while(numfour <= 50){
	if(numfour%5 == 0 && numfour%3 == 0){
		console.log(numfour);
	}
	numfour++;
}