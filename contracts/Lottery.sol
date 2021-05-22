pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {
    using SafeMathChainlink for uint256;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE { OPEN, CLOSED, CALCULATING_WINNER }
    LOTTERY_STATE public lottery_state;
    uint256 public lotteryId;
    address payable[] public players;
    address public recentWinner;
    // 0.1 LINK
    uint256 public fee = 100000000000000000;
    uint256 public usdEntryFee;
    bytes32 public keyHash;
    uint256 public randomness;
    event RequestedRandomness(bytes32 requestId);

    constructor(address ethUsdPriceFeedAddress, address _vrfCoordinator, address _link, bytes32 _keyHash) 
        VRFConsumerBase(
            _vrfCoordinator, // VRF Coordinator
            _link  // LINK Token
        ) public
    {   
        ethUsdPriceFeed = AggregatorV3Interface(ethUsdPriceFeedAddress);
        lotteryId = 1;
        lottery_state = LOTTERY_STATE.CLOSED;
        keyHash = _keyHash;
        usdEntryFee = 50;
    }

    function enter() public payable {
        require(msg.value >= getEntranceFee(), "Not enough ETH to enter!");
        require(lottery_state == LOTTERY_STATE.OPEN);
        players.push(msg.sender);
    } 

    function getEntranceFee() public view returns(uint256){
        uint256 precision = 1 * 10 ** 36; 
        uint256 price = getLatestEthUsdPrice(); // 2000_000000000000000000
        // uint256 costToEnter = usdEntryFee * 10 ** 18 / price; This would be 0.25
        uint256 costToEnter = usdEntryFee * precision / price; 
        return costToEnter;
    }

    function getLatestEthUsdPrice() public view returns (uint256) {
        (,int price,,,) = ethUsdPriceFeed.latestRoundData();
        price = price * 10000000000;
        return uint256(price);
    }
    
    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, "can't start a new lottery yet");
        lottery_state = LOTTERY_STATE.OPEN;
        randomness = 0;
    }

    function endLottery(uint256 userProvidedSeed) public onlyOwner {
      require(lottery_state == LOTTERY_STATE.OPEN, "Can't end a lottery that hasnt started!");
      lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
      pickWinner(userProvidedSeed);
    }


    function pickWinner(uint256 userProvidedSeed) private returns (bytes32){
        // DONT do something like this:
        // uint(keccak256(abi.encodePacked(nonce, msg.sender, block.difficulty, block.timestamp))) % players.length;
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "You aren't at that stage yet!");
        bytes32 requestId = requestRandomness(keyHash, fee, userProvidedSeed);
        emit RequestedRandomness(requestId);
    }
    
    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "You aren't at that stage yet!");
        require(randomness > 0, "random-not-found");
        uint256 index = randomness % players.length;
        recentWinner = players[index];
        players[index].transfer(address(this).balance);
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = randomness;
    }

    function get_players() public view returns (address payable[] memory) {
        return players;
    }
    
    function get_pot() public view returns(uint256){
        return address(this).balance;
    }
}
