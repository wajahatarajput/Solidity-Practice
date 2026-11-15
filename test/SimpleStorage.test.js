const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleStorage", function () {
  it("stores and retrieves a number", async function () {
    const SimpleStorage = await ethers.getContractFactory("SimpleStorage");
    const storage = await SimpleStorage.deploy();
    await storage.waitForDeployment();

    await storage.set(42);
    expect(await storage.get()).to.equal(42n);
  });

  it("emits NumberUpdated", async function () {
    const SimpleStorage = await ethers.getContractFactory("SimpleStorage");
    const storage = await SimpleStorage.deploy();
    await storage.waitForDeployment();

    await expect(storage.set(7))
      .to.emit(storage, "NumberUpdated")
      .withArgs(0n, 7n);
  });
});
