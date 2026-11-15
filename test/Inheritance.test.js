const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Inheritance (Dog)", function () {
  it("overrides speak and describe", async function () {
    const Dog = await ethers.getContractFactory("Dog");
    const dog = await Dog.deploy("Rex");
    await dog.waitForDeployment();

    expect(await dog.name()).to.equal("Rex");
    expect(await dog.speak()).to.equal("woof");
    expect(await dog.describe()).to.equal("Dog: Rex");
  });
});

describe("MultipleInheritance (D)", function () {
  it("follows C3 linearization via super", async function () {
    const D = await ethers.getContractFactory("D");
    const d = await D.deploy();
    await d.waitForDeployment();

    // D is B, C → super path: D <- C <- B <- A
    expect(await d.greet()).to.equal("A -> B -> C -> D");
  });
});
