

# Remove database
rm -rf database/db.db
rm -rf database/files/*
mkdir database/files

# Remove merkle tree archive
rm -rf merkletree/tree_archive/*
mkdir merkletree/tree_archive/


# Remove uploads
rm -rf uploads/*

rm -rf signtool/keys/*
mkdir signtool/keys/

# (Optional) remove wallet 
clw --wallet-remove Catena
