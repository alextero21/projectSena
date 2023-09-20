function generateRandomName() {
  const adjectives = ["Happy", "Clever", "Brave", "Creative", "Energetic", "Gentle", "Curious"];
  const nouns = ["Cat", "Dog", "Elephant", "Lion", "Tiger", "Monkey", "Bear", "Dolphin", "Penguin", "Kangaroo"];

  const randomAdjective = adjectives[Math.floor(Math.random() * adjectives.length)];
  const randomNoun = nouns[Math.floor(Math.random() * nouns.length)];

  const randomName = randomAdjective + " " + randomNoun;
  return randomName;
}

$(document).ready(function () {
  
  $('#alerta').click(function (e) { 
    e.preventDefault();
    console.log('GOLA');
    $(".alert").alert()
    
  });
});