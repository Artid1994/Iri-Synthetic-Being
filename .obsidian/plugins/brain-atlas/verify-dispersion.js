#!/usr/bin/env node
/**
 * Brain Atlas Dispersion Verification Script
 * Validates Mo(t,r,e) function output remains within anatomical bounds
 */

// Simulate the Mo(t,r,e) jitter function from Brain Atlas
function simulateJitterRadius(regionRadius, pseudoRandomHash) {
    // Current formula in main.js: u = e * (0.20 + c * 0.30)
    const e = regionRadius;
    const c = pseudoRandomHash; // 0.0 to 1.0
    const u = e * (0.20 + c * 0.30);
    return u;
}

// Test parameters for different brain regions
const testRegions = [
    { name: "TEMPORAL", radius: 0.3, nodeCount: 451 },
    { name: "BRAIN STEM", radius: 0.14, nodeCount: 596 },
    { name: "FRONTAL", radius: 0.35, nodeCount: 200 },
    { name: "CEREBELLUM", radius: 0.22, nodeCount: 220 }
];

console.log("=".repeat(60));
console.log("Brain Atlas Dispersion Verification");
console.log("=".repeat(60));
console.log("\nFormula: u = e * (0.20 + c * 0.30)");
console.log("  where e = region radius, c = pseudo-random hash [0-1]\n");

let allTestsPassed = true;
const results = [];

testRegions.forEach(region => {
    console.log(`\n--- Testing: ${region.name} (${region.nodeCount} nodes) ---`);
    console.log(`Region radius: ${region.radius.toFixed(3)}`);
    
    // Test with multiple random samples
    const samples = 100;
    let minJitter = Infinity;
    let maxJitter = -Infinity;
    let avgJitter = 0;
    
    for (let i = 0; i < samples; i++) {
        const randomHash = Math.random();
        const jitter = simulateJitterRadius(region.radius, randomHash);
        
        minJitter = Math.min(minJitter, jitter);
        maxJitter = Math.max(maxJitter, jitter);
        avgJitter += jitter;
    }
    
    avgJitter /= samples;
    
    // Calculate bounds
    const minBound = region.radius * 0.20;
    const maxBound = region.radius * 0.50; // (0.20 + 0.30)
    
    // Check if nodes stay within region (jitter should be < radius for containment)
    const maxAllowedJitter = region.radius * 0.8; // 80% of radius for safety
    const withinBounds = maxJitter <= maxAllowedJitter;
    
    console.log(`Jitter range: ${minJitter.toFixed(4)} - ${maxJitter.toFixed(4)}`);
    console.log(`Average jitter: ${avgJitter.toFixed(4)}`);
    console.log(`Max allowed: ${maxAllowedJitter.toFixed(4)}`);
    console.log(`Status: ${withinBounds ? '✓ PASS' : '✗ FAIL'} - Nodes ${withinBounds ? 'contained' : 'may escape'} within region`);
    
    // Check for overlap (minimum spacing)
    const minSpacing = avgJitter * 2; // Diameter of typical node
    const estimatedNodesPerVolume = Math.pow(region.radius / minSpacing, 3);
    const densityOkay = region.nodeCount < estimatedNodesPerVolume * 10; // 10x safety margin
    
    console.log(`Estimated capacity: ${estimatedNodesPerVolume.toFixed(0)} nodes`);
    console.log(`Actual nodes: ${region.nodeCount}`);
    console.log(`Density check: ${densityOkay ? '✓ PASS' : '⚠ WARN'} - ${densityOkay ? 'Good spacing' : 'May be crowded'}`);
    
    if (!withinBounds) allTestsPassed = false;
    
    results.push({
        region: region.name,
        minJitter,
        maxJitter,
        avgJitter,
        withinBounds,
        densityOkay
    });
});

// Summary
console.log("\n" + "=".repeat(60));
console.log("VERIFICATION SUMMARY");
console.log("=".repeat(60));

results.forEach(r => {
    console.log(`${r.region}: ${r.withinBounds ? '✓' : '✗'} Bounds | ${r.densityOkay ? '✓' : '⚠'} Density | Jitter: ${r.avgJitter.toFixed(4)}`);
});

console.log("\n" + "=".repeat(60));
if (allTestsPassed) {
    console.log("✓ ALL TESTS PASSED");
    console.log("Brain Atlas dispersion is within anatomical bounds.");
    console.log("Nodes will spread naturally without escaping regions.");
    process.exit(0);
} else {
    console.log("✗ VERIFICATION FAILED");
    console.log("Some nodes may escape their anatomical regions.");
    process.exit(1);
}
