import mongoose from "mongoose";
import User from "../models/user.js";

const USER3_EMAIL = "user3@fitpal.com";
const USER3_PASSWORD = "Password123!";

const addPartialProfileUser = async () => {
  const mongoUri = process.env.MONGODB_CONNECTION_STRING;

  if (!mongoUri) {
    throw new Error("Missing MONGODB_CONNECTION_STRING in environment.");
  }

  await mongoose.connect(mongoUri);
  console.log("Connected to database.");

  const existing = await User.findOne({ email: USER3_EMAIL });

  if (existing) {
    console.log(`User already exists: ${USER3_EMAIL}`);
    console.log("No changes made. Existing data preserved.");
  } else {
    await User.create({
      email: USER3_EMAIL,
      password: USER3_PASSWORD,
      firstName: "Alex",
      lastName: "Rivera",
      gender: "Female",
      dob: new Date("2000-03-22"),
      deactivated: false,
      favouriteFood: [],
    });
    console.log("Created partial-profile user.");
  }

  console.log(`Email: ${USER3_EMAIL}`);
  console.log(`Password: ${USER3_PASSWORD}`);
  console.log("Profile: firstName, lastName, gender, dob set; no profile picture or physical info.");

  await mongoose.disconnect();
  console.log("Disconnected from database.");
};

addPartialProfileUser().catch(async (error) => {
  console.error("Failed to add partial-profile user:", error);
  try {
    await mongoose.disconnect();
  } catch {
    // ignore disconnect errors
  }
  process.exit(1);
});
