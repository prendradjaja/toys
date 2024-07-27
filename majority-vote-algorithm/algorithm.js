// algorithm.js created largely by generative AI

function findMajorityElement(nums) {
  // Phase 1: Find the candidate
  let candidate = null;
  let count = 0;

  for (const num of nums) {
    if (count === 0) {
      candidate = num;
    }
    count += (num === candidate) ? 1 : -1;
  }

  // Phase 2: Verify the candidate
  count = 0;
  for (const num of nums) {
    if (num === candidate) {
      count++;
    }
  }

  // Check if candidate is actually the majority element
  if (count > nums.length / 2) {
    return candidate;
  } else {
    return null; // No majority element
  }
}

function getAlgorithmStates(nums) {
  // Phase 1: Find the candidate
  let m = null;
  let c = 0;

  const states = [
    {x: 0, y: 0, color: white, dotted: true},
  ];

  let x = 0;

  for (const num of nums) {
    if (c === 0) {
      m = num;
    }
    c += (num === m) ? 1 : -1;
    x++;
    states.push({
      x,
      y: c,
      color: m,
    });
  }

  return states;
}
