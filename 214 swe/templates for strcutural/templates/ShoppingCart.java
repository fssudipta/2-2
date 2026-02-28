interface PaymentProcessor{
    void pay(double amount);
}

class LegacyBankAPI{
    public void transferMoney(double amount, String currency){
        System.out.println("Processing $"+amount+" via the bank API in "+currency);
    }
}

// the adapter bridges the gap
class BankAdapter implements PaymentProcessor{
    private LegacyBankAPI bankAPI;
    public BankAdapter(LegacyBankAPI bankAPI){
        this.bankAPI=bankAPI;
    }
    @Override
    public void pay(double amount){
        // converting the call to what the bank expects
        String currency = "usd";
        bankAPI.transferMoney(amount, currency);
    }
}

public class ShoppingCart{
    public static void main(String[] args) {
        LegacyBankAPI legacyBank = new LegacyBankAPI(); // creating legacy bank srvc
        PaymentProcessor processor = new BankAdapter(legacyBank);//wrap it around the adapter
        processor.pay(100.00);
    }
}