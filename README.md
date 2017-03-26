# fraud-alert
A service that uses an SVM to determine whether there are fraudulent charges on a credit card account, and texts the owner if any are found. Built at MHacks 9 by Timothy Tamm and Abby Lyons.

To use, create a file called secret.json that includes your Nessie key and customer ID, Twilio sid, token, and number, and the phone number that should receive the texts. 