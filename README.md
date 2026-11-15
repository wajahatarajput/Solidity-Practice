# Solidity Practice Curriculum

A progressive Hardhat project with focused Solidity contracts covering **basics → OOP → advanced patterns → tokens**. Each file teaches one idea with NatSpec comments. Practice contracts are for learning — **not production**.

## Prerequisites

- [Node.js](https://nodejs.org/) 18+ and npm
- Optional: [Remix IDE](https://remix.ethereum.org/) (browser, no install)
- Optional: `solc` / `solcjs` for CLI compilation

## Quick start (Hardhat)

```bash
npm install
npx hardhat compile
npx hardhat test
npx hardhat run scripts/deploy.js
```

Or use the npm scripts:

```bash
npm run compile
npm run test
npm run deploy
```

## Project structure

```
Solidity-Practice/
├── contracts/
│   ├── 01-basics/
│   ├── 02-types-and-data/
│   ├── 03-functions-control/
│   ├── 04-oop/
│   ├── 05-events-errors-modifiers/
│   ├── 06-advanced/
│   └── 07-tokens/
├── scripts/deploy.js
├── test/
├── hardhat.config.js
└── package.json
```

Compiler version: **Solidity 0.8.24** (see `hardhat.config.js`).

---

## Ways to compile

### 1. Hardhat (recommended)

Compiles every contract under `contracts/`, writes ABIs and bytecode to `artifacts/`.

```bash
npm install
npx hardhat compile
```

Useful commands:

| Command | Purpose |
|--------|---------|
| `npx hardhat compile` | Compile all contracts |
| `npx hardhat clean` | Delete cache and artifacts |
| `npx hardhat test` | Run Mocha/Chai tests |
| `npx hardhat run scripts/deploy.js` | Deploy sample contracts (local network) |
| `npx hardhat node` | Start a local JSON-RPC node |

### 2. Remix IDE

1. Open [https://remix.ethereum.org](https://remix.ethereum.org)
2. Create a new file and paste any `.sol` from this repo (or use Remix’s file explorer to upload)
3. In the **Solidity Compiler** tab, set compiler to **0.8.24**
4. Click **Compile**
5. Use the **Deploy & Run** tab to deploy to the Remix VM or an injected wallet

Remix tip: if a file references another contract in the same file (e.g. inheritance examples), paste the whole file — Remix compiles the selected file and its in-file dependencies.

### 3. solc / solcjs CLI

Using the npm package (no global install required):

```bash
npx solcjs --bin --abi --optimize --base-path . contracts/01-basics/HelloWorld.sol -o build/
```

Notes:

- Multi-file projects with imports need `--base-path` / `--include-path`
- Match the pragma: use `0.8.24` (or compatible `^0.8.24`)
- Hardhat is easier for this repo because everything already lives under one `contracts/` tree

---

## Concept explanations

Work through folders in order. Open each `.sol`, read this section, then try the exercises.

---

### 01 — Basics

#### What is a smart contract?

A **contract** is like a class that lives on the blockchain. Once deployed, its code and storage are public and permanent (until the contract self-destructs, which modern practice avoids). Users call **functions** by sending transactions. Functions that only read state can be called without a transaction (a free `eth_call`).

Every `.sol` file starts with:

- `SPDX-License-Identifier` — license for the source
- `pragma solidity ^0.8.24;` — which compiler versions are allowed

#### `HelloWorld.sol` — state and getters

**State variables** are stored on-chain between calls. `string public greeting` both stores data and auto-creates a getter named `greeting()`.

The **constructor** runs once at deploy time to set initial state. `setGreeting` mutates storage (costs gas). `getGreeting` is `view` — it reads but does not write.

**Try:** Deploy with `"Hello, Solidity!"`, call `getGreeting`, then `setGreeting("Hi")`.

#### `SimpleStorage.sol` — read/write storage

Shows the classic pattern: private state + public setter/getter. Emitting an **event** (`NumberUpdated`) lets wallets and indexers notice changes without scanning all storage.

**Try:** `set(42)` then `get()`. In Remix or Hardhat logs, find the `NumberUpdated` event.

---

### 02 — Types and data

#### Value types vs reference types

| Kind | Examples | Behavior |
|------|----------|----------|
| **Value types** | `uint`, `int`, `bool`, `address`, `bytes32`, `enum` | Copied when assigned or passed |
| **Reference types** | arrays, `struct`, `mapping`, `string`, `bytes` | Point at data; you must name a **data location** |

#### `ValueTypes.sol`

- **`uint256` / `int256`** — unsigned / signed integers. `uint` is alias for `uint256`. Solidity 0.8+ reverts on overflow/underflow by default.
- **`bool`** — `true` / `false`.
- **`address`** — 20-byte account or contract ID. `payable address` can receive ETH.
- **`bytes32`** — fixed 32-byte blob (hashes fit here). **`bytes`** — dynamic byte array.
- **`enum`** — named set of constants (stored as small integers under the hood).

**Try:** Change `Status`, toggle `flag`, set a new `owner`.

#### `ReferenceTypes.sol`

- **Arrays** — `uint256[]` grows with `push`. Fixed-size arrays exist too (`uint256[3]`).
- **Structs** — group fields (`Person { name, age, wallet }`).
- **Mappings** — `mapping(key => value)` hash tables. Keys are not iterable; missing keys return the zero value.
- **Nested mappings** — e.g. `allowances[owner][spender]` (ERC-20 style).

**Try:** `addPerson`, `setBalance`, set a nested allowance.

#### `DataLocations.sol` — storage, memory, calldata

For reference types you must pick where data lives:

| Location | Lifetime | Mutable? | Typical use |
|----------|----------|----------|-------------|
| **`storage`** | Permanent (contract state) | Yes | State variables; pointers into state |
| **`memory`** | During the call only | Yes | Temporary copies, return values |
| **`calldata`** | During the call only | No (read-only) | `external` function inputs (cheapest) |

`Item storage ref = items[0]` **aliases** on-chain data — changing `ref` writes state. `Item memory copy = items[0]` is a **snapshot** — changing `copy` does not persist.

**Try:** `addItem`, then `updateFirst`. Read `items(0)` — name/quantity updated; the `+1` on `memCopy` is gone.

---

### 03 — Functions and control

#### `Visibility.sol`

Who can call a function (or read a state variable):

| Visibility | Meaning |
|------------|---------|
| **`public`** | Inside + outside; state vars get an auto getter |
| **`external`** | Only from outside (or via `this.fn()`); good for large calldata args |
| **`internal`** | This contract + contracts that inherit it |
| **`private`** | Only this contract (not children) |

**Try:** Deploy `VisibilityChild` and call `readInternal` / `callParentInternal`. Calling `privateFn` from outside should fail to appear in the ABI.

#### `ViewPurePayable.sol`

| Keyword | Meaning |
|---------|---------|
| **`pure`** | No read or write of state (only args + locals) |
| **`view`** | May read state; must not modify it |
| **`payable`** | Function may receive ETH (`msg.value`) |

Special functions:

- **`receive()`** — called on plain ETH transfers (empty calldata). Must be `external payable`.
- **`fallback()`** — called when no function matches, or when calldata is non-empty and unmatched. Can be `payable`.

**Try:** Call `add` (pure), `getBalance` (view), `deposit` with value, and send bare ETH to trigger `receive`.

#### `ControlFlow.sol`

Standard `if` / `else`, `for`, `while`. Error handling:

| Tool | Use |
|------|-----|
| **`require(cond, "msg")`** | Validate inputs / conditions; refunds remaining gas |
| **`revert("msg")`** | Unconditional abort with message |
| **`assert(cond)`** | Internal invariants; on failure uses Panic (should “never” happen) |

Prefer **custom errors** (module 05) over long require strings for gas.

**Try:** `classify(3)`, `sumTo(10)`, `mustBePositive(-1)` (should revert).

---

### 04 — OOP in Solidity

Solidity is **contract-oriented**. Classic OOP ideas still apply:

| OOP idea | Solidity tool |
|----------|----------------|
| Inheritance | `contract Child is Parent` |
| Polymorphism | `virtual` / `override`, base-type parameters |
| Abstract classes | `abstract contract` |
| Interfaces | `interface` |
| Encapsulation | private/internal state + getters + modifiers |
| Utilities | `library` + `using Lib for Type` |

#### Inheritance (`Inheritance.sol`)

`Dog is Animal` means Dog gets Animal’s members. Mark parent functions **`virtual`** so children can **`override`** them. Parent constructors are called like `Animal(_name)` in the child’s constructor list.

**Try:** Deploy `Dog("Rex")`. `speak()` returns `"woof"`, not `"..."`.

#### Multiple inheritance (`MultipleInheritance.sol`)

A contract can inherit several parents: `contract D is B, C`. If both define the same function, you must write `override(B, C)` and Solidity uses **C3 linearization** (similar to Python) to order `super` calls. With `D is B, C`, the `super` chain is roughly **D → C → B → A**.

**Try:** Deploy `D`, call `greet()` → `"A -> B -> C -> D"`.

#### Abstract contracts (`AbstractContracts.sol`)

An **`abstract contract`** has at least one function without a body (or is marked abstract). You cannot deploy it until a child implements everything. Useful for shared logic + required hooks (`area()`).

**Try:** Deploy `Rectangle(3, 4)` and `Circle(10)`; compare `area()` and `name()`.

#### Interfaces (`Interfaces.sol`)

An **`interface`** lists function signatures only (all implicitly `external`). No state variables, no constructors. Any contract that implements the functions can be used wherever the interface type is expected — **loose coupling**.

**Try:** Deploy `Counter` and `CounterUser`, then `bumpTwice(counterAddress)`.

#### Polymorphism (`Polymorphism.sol`)

Same call site, different behavior. `Checkout.checkout(PaymentMethod method, ...)` accepts any child of `PaymentMethod`. Calling `method.pay(...)` runs the **override** on the concrete contract (`CashPayment` vs `CardPayment`).

**Try:** Deploy both payment contracts + `Checkout`; call `checkout` with each address.

#### Encapsulation (`Encapsulation.sol`)

Hide internals (`private balance`, `private owner`) and expose safe operations (`deposit`, `withdraw` with `onlyOwner`). Outside code cannot assign `balance` directly — only through your functions. That is OOP **encapsulation** on-chain.

**Try:** Deposit from any account; withdraw only from the owner account.

#### Libraries (`Libraries.sol`)

A **`library`** is reusable code, often inlined when functions are `internal`. `using MathLib for uint256` lets you write `a.max(b)` instead of `MathLib.max(a, b)`. Libraries do not hold contract storage of their own in the usual pattern.

**Try:** Call `bigger`, `bounded`, `total` on `LibraryDemo`.

---

### 05 — Events, errors, modifiers

#### Modifiers (`Modifiers.sol`)

A **modifier** wraps a function with shared checks. The `_` placeholder is where the function body runs:

```solidity
modifier onlyOwner() {
    require(msg.sender == owner, "not owner");
    _;
}
```

You can stack modifiers: `onlyOwner whenNotPaused validAmount(amount)`.

**Try:** `setPaused(true)`, then `setValue(5)` — should revert with `"paused"`.

#### Events (`Events.sol`)

**Events** write cheap logs (not contract storage). Off-chain apps subscribe to them. Up to **three** parameters can be **`indexed`** (searchable topics). Non-indexed data is in the log payload.

**Try:** `transfer` tokens (internal balances) and inspect the `Transfer` log in Remix.

#### Custom errors (`CustomErrors.sol`)

```solidity
error InsufficientBalance(uint256 available, uint256 required);
// ...
revert InsufficientBalance(available, amount);
```

Custom errors cost **less gas** than `require(..., "long string")` and can carry typed fields for better UX in wallets/UIs.

**Try:** Call `withdraw` with more than your balance and decode the error.

---

### 06 — Advanced

#### Constructor, constant, immutable (`ConstructorImmutable.sol`)

- **Constructor** — runs once at deployment.
- **`constant`** — value fixed at compile time; no storage slot.
- **`immutable`** — set in the constructor, then forever read-only; also cheaper than regular storage reads.

**Try:** Deploy and read `deployer`, `createdAt`, `MAX_SUPPLY`.

#### Ether handling (`EtherWallet.sol`)

Contracts receive ETH via `payable` functions, `receive`, or `fallback`. To send ETH out, prefer:

```solidity
(bool ok, ) = payable(to).call{value: amount}("");
require(ok, "call failed");
```

`transfer`/`send` forward only 2300 gas and can break with modern recipients. Always think about **reentrancy** when sending value (see `SecurityPatterns.sol`).

**Try:** Deposit ETH, then `withdraw` as owner.

#### `call` vs `delegatecall` (`CallDelegatecall.sol`)

| Method | Code runs from | Storage used | Typical use |
|--------|----------------|--------------|-------------|
| **`call`** | Target contract | Target’s storage | Normal external calls |
| **`delegatecall`** | Target contract | **Caller’s** storage | Proxies / upgradeable patterns |

`delegatecall` to an untrusted contract is dangerous — it can overwrite your storage layout.

**Try:** Deploy `Logic` + `Caller`. Use `callSetNumber` (Logic’s `number` changes). Use `delegateSetNumber` (Caller’s `number` changes).

#### Assembly / Yul (`AssemblyBasics.sol`)

**Inline assembly** lets you use Yul for low-level ops (`add`, `sstore`, `sload`, `extcodesize`). Use sparingly — easy to break safety checks Solidity normally gives you.

**Try:** `storeAssembly(99)` then `loadAssembly()`.

#### Security patterns (`SecurityPatterns.sol`)

Two essentials:

1. **Checks → Effects → Interactions (CEI)** — validate, update your state, *then* call other contracts.
2. **Reentrancy guard** — a `locked` flag (`nonReentrant`) so an external call cannot re-enter `withdraw` before it finishes.

**Try:** Deposit, withdraw; notice balance is reduced *before* the ETH `call`.

---

### 07 — Tokens

#### Fungible tokens — ERC-20 (`SimpleERC20.sol`)

**ERC-20** is the standard for interchangeable tokens (stablecoins, governance tokens, etc.). Core ideas:

| Piece | Role |
|-------|------|
| `balanceOf` | How many tokens an address holds |
| `transfer` | Send your tokens |
| `approve` + `allowance` | Let a spender move tokens for you |
| `transferFrom` | Spender moves tokens within allowance |
| `Transfer` / `Approval` events | Required logs for indexers |

This repo’s version is a **minimal learning implementation** (no OpenZeppelin). Production apps should use audited libraries.

**Try:** Transfer to another account; `approve` then `transferFrom` (covered by `test/SimpleERC20.test.js`).

#### NFTs — ERC-721 (`SimpleERC721.sol`)

**ERC-721** tokens are unique (`tokenId`). Each ID has one owner. Core ideas:

| Piece | Role |
|-------|------|
| `ownerOf(tokenId)` | Who owns this NFT |
| `balanceOf(owner)` | How many NFTs they hold |
| `mint` | Create a new ID (learning helper) |
| `approve` / `transferFrom` | Authorize and move a specific ID |

Again: simplified for teaching, not a full production NFT.

**Try:** `mint(yourAddress)`, then `transferFrom` to another address.

---

## Learning path checklist

| # | File | Concept |
|---|------|---------|
| 1 | `01-basics/HelloWorld.sol` | First contract, state, getter/setter |
| 2 | `01-basics/SimpleStorage.sol` | Storage + events |
| 3 | `02-types-and-data/ValueTypes.sol` | Integers, bool, address, bytes, enum |
| 4 | `02-types-and-data/ReferenceTypes.sol` | Arrays, structs, mappings |
| 5 | `02-types-and-data/DataLocations.sol` | storage / memory / calldata |
| 6 | `03-functions-control/Visibility.sol` | public / private / internal / external |
| 7 | `03-functions-control/ViewPurePayable.sol` | view, pure, payable, receive/fallback |
| 8 | `03-functions-control/ControlFlow.sol` | if/loops, require/assert/revert |
| 9 | `04-oop/Inheritance.sol` | Single inheritance, virtual/override |
| 10 | `04-oop/MultipleInheritance.sol` | Diamond + C3 linearization |
| 11 | `04-oop/AbstractContracts.sol` | Abstract base contracts |
| 12 | `04-oop/Interfaces.sol` | Interfaces + loose coupling |
| 13 | `04-oop/Polymorphism.sol` | Runtime dispatch via overrides |
| 14 | `04-oop/Encapsulation.sol` | Private state + controlled API |
| 15 | `04-oop/Libraries.sol` | Libraries and `using for` |
| 16 | `05-events-errors-modifiers/Modifiers.sol` | Function modifiers |
| 17 | `05-events-errors-modifiers/Events.sol` | Indexed events |
| 18 | `05-events-errors-modifiers/CustomErrors.sol` | Custom errors |
| 19 | `06-advanced/ConstructorImmutable.sol` | constant / immutable |
| 20 | `06-advanced/EtherWallet.sol` | Sending/receiving ETH |
| 21 | `06-advanced/CallDelegatecall.sol` | call vs delegatecall |
| 22 | `06-advanced/AssemblyBasics.sol` | Inline assembly (Yul) |
| 23 | `06-advanced/SecurityPatterns.sol` | CEI + reentrancy guard |
| 24 | `07-tokens/SimpleERC20.sol` | Fungible token standard |
| 25 | `07-tokens/SimpleERC721.sol` | NFT-style token |

---

## Tests

```bash
npx hardhat test
```

| Test file | Covers |
|-----------|--------|
| `test/SimpleStorage.test.js` | set/get + event |
| `test/Inheritance.test.js` | `Dog` override + diamond `D.greet()` |
| `test/SimpleERC20.test.js` | mint, transfer, approve/`transferFrom` |

## Deploy script

`scripts/deploy.js` deploys `HelloWorld`, `SimpleStorage`, and `SimpleERC20` to the Hardhat network:

```bash
npx hardhat run scripts/deploy.js
```

To deploy against a persistent local node:

```bash
npx hardhat node
# in another terminal:
npx hardhat run scripts/deploy.js --network localhost
```

---

## Solidity OOP cheat sheet

```solidity
// Inheritance + polymorphism
contract Base {
    function foo() public pure virtual returns (string memory) { return "base"; }
}
contract Child is Base {
    function foo() public pure override returns (string memory) { return "child"; }
}

// Abstract (cannot deploy until complete)
abstract contract Shape {
    function area() public view virtual returns (uint256);
}

// Interface (signatures only)
interface ICounter {
    function increment() external;
}

// Library
library MathLib {
    function max(uint256 a, uint256 b) internal pure returns (uint256) {
        return a >= b ? a : b;
    }
}
```

## Safety note

These contracts intentionally keep logic small and visible. They omit production hardening (full ERC compliance, audited access control, upgrade safety, etc.). Do not deploy them to mainnet with real funds.

## License

MIT
