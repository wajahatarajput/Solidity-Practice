const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleERC20", function () {
  async function deployToken() {
    const [owner, alice] = await ethers.getSigners();
    const SimpleERC20 = await ethers.getContractFactory("SimpleERC20");
    const token = await SimpleERC20.deploy(
      "Practice Token",
      "PRAC",
      ethers.parseEther("1000")
    );
    await token.waitForDeployment();
    return { token, owner, alice };
  }

  it("mints initial supply to deployer", async function () {
    const { token, owner } = await deployToken();
    expect(await token.balanceOf(owner.address)).to.equal(
      ethers.parseEther("1000")
    );
    expect(await token.totalSupply()).to.equal(ethers.parseEther("1000"));
  });

  it("transfers tokens", async function () {
    const { token, owner, alice } = await deployToken();
    const amount = ethers.parseEther("50");

    await token.transfer(alice.address, amount);

    expect(await token.balanceOf(alice.address)).to.equal(amount);
    expect(await token.balanceOf(owner.address)).to.equal(
      ethers.parseEther("950")
    );
  });

  it("approves and transferFrom", async function () {
    const { token, owner, alice } = await deployToken();
    const amount = ethers.parseEther("25");

    await token.approve(alice.address, amount);
    await token.connect(alice).transferFrom(owner.address, alice.address, amount);

    expect(await token.balanceOf(alice.address)).to.equal(amount);
  });
});
