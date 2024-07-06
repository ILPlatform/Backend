import firebase from "firebase/compat/app";
import { getFunctions, connectFunctionsEmulator, httpsCallable } from "firebase/functions";
import { getAuth } from "firebase/auth";
import "firebase/compat/firestore";

// Initialize Firebase
const app = firebase.initializeApp({
  apiKey: "AIzaSyBivMgQF_uNn7gm9-UwSRkm1CBVimMrrRo",
  authDomain: "ilplatform.firebaseapp.com",
  projectId: "ilplatform",
  storageBucket: "ilplatform.appspot.com",
  messagingSenderId: "482052945832",
  appId: "1:482052945832:web:d80ac5ab412b3e82dfcf9d",
  measurementId: "G-SR7EQBVXCX",
});

// Connect to Firebase Auth
const auth = getAuth(app);

// Connect to Firebase Functions
const functions = getFunctions(app, "europe-west1");
if (process.env.NODE_ENV === "development") {
  connectFunctionsEmulator(functions, "localhost", 5001);
}

// Function to call a Firebase Function
const callFunction = (functionName) => httpsCallable(functions, functionName);

export { callFunction, auth };
