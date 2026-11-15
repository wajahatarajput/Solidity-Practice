const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const HelloWorld = await hre.ethers.getContractFactory("HelloWorld");
  const hello = await HelloWorld.deploy("Hello, Solidity!");
  await hello.waitForDeployment();
  console.log("HelloWorld:", await hello.getAddress());

  const SimpleStorage = await hre.ethers.getContractFactory("SimpleStorage");
  const storage = await SimpleStorage.deploy();
  await storage.waitForDeployment();
  console.log("SimpleStorage:", await storage.getAddress());

  const SimpleERC20 = await hre.ethers.getContractFactory("SimpleERC20");
  const token = await SimpleERC20.deploy(
    "Practice Token",
    "PRAC",
    hre.ethers.parseEther("1000000")
  );
  await token.waitForDeployment();
  console.log("SimpleERC20:", await token.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
