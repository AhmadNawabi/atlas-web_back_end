export function taskFirst () {
  const tast = 'I prefer const when I can.';
  return tast;
}

export function getLast () {
  return ' is okay ';
}

export function tastNext () {
  let combination = 'But sometimes let';
  combination += getLast();

  return combination;
}
