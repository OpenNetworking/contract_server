contract Information{
    uint bal;
    function bet(){
	bal=10;
    }
    function Information()
    {
	address info_adr = 0x50;
	info_adr.send(50,60);

    }
}