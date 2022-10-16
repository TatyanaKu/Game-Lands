db.createUser(
    {
        user    : "game-lands",
        pwd     : "game-lands",
        roles   : [
            {
                role: "readWrite",
                db  : "game-lands"
            }
        ]    
    }
)