interface DatabaseQuery {
    void executeQuery(String query);
}

class SQLDatabase implements DatabaseQuery { //kono kajer jinish na, just matha ghuranor jonno dewa
    @Override
    public void executeQuery(String sqlQuery) {
        System.out.println("Executing SQL query: " + sqlQuery);
    }
}

class NoSQLDatabase {
    public void runQuery(String noSQLQuery) {
        System.out.println("Executing NoSQL query: " + noSQLQuery);
    }
}

class NoSQLAdapter implements DatabaseQuery {

    private NoSQLDatabase noSQLDatabase;

    public NoSQLAdapter(NoSQLDatabase noSQLDatabase) {
        this.noSQLDatabase = noSQLDatabase;
    }

    @Override
    public void executeQuery(String query) {
        // Translate SQL-style call to NoSQL call
        noSQLDatabase.runQuery(query);
    }
}


public class online_secC2 {
    public static void main(String[] args) {

        // Existing SQL database
        DatabaseQuery sqlDB = new SQLDatabase();
        sqlDB.executeQuery("SELECT * FROM users");

        // New NoSQL database (through adapter)
        NoSQLDatabase noSQLDatabase = new NoSQLDatabase();
        DatabaseQuery noSQLAdapter =
                new NoSQLAdapter(noSQLDatabase);

        noSQLAdapter.executeQuery("{ find: 'users' }");
    }
}
