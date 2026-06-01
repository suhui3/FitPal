import mongoose from "mongoose";
import User from "../models/user.js";
import ExerciseLog from "../models/exercise.js";
import FoodDiary from "../models/foodDiary.js";
import Reminder from "../models/reminder.js";

const USER1_EMAIL = "user1@fitpal.com";
const USER1_PASSWORD = "Password123!";
const USER2_EMAIL = "user2@fitpal.com";
const USER2_PASSWORD = "Password123!";
const PERFORMANCE_SEED_DAYS = 540;

const toDateKey = (date) => {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
};

const startOfDay = (dateKey) => new Date(dateKey);

const dateFromToday = (offsetDays) => {
  const d = new Date();
  d.setHours(0, 0, 0, 0);
  d.setDate(d.getDate() + offsetDays);
  return d;
};

const buildDemoMealsForDay = (dateKey, dayIndex) => {
  const cycle = dayIndex % 30;
  const wave = Math.floor(cycle / 10);

  const breakfastBase = {
    mealId: 100000 + dayIndex * 10 + 1,
    foodName: `Oatmeal Bowl ${dayIndex + 1}`,
    imageUrl: "https://img.spoonacular.com/recipes/716429-312x231.jpg",
    calories: 400 + (cycle % 4) * 20 + wave * 8,
    protein: 25,
    fat: 12,
    carbs: 52,
    mealType: "breakfast",
  };

  const lunchBase = {
    mealId: 100000 + dayIndex * 10 + 2,
    foodName: `Chicken Rice Bowl ${dayIndex + 1}`,
    imageUrl: "https://img.spoonacular.com/recipes/715538-312x231.jpg",
    calories: 530 + (cycle % 5) * 18 + wave * 12,
    protein: 38,
    fat: 18,
    carbs: 58,
    mealType: "lunch",
  };

  const dinnerBase = {
    mealId: 100000 + dayIndex * 10 + 3,
    foodName: `Salmon Veg Plate ${dayIndex + 1}`,
    imageUrl: "https://img.spoonacular.com/recipes/782585-312x231.jpg",
    calories: 590 + (cycle % 6) * 16 + wave * 10,
    protein: 42,
    fat: 24,
    carbs: 46,
    mealType: "dinner",
  };

  return {
    date: startOfDay(dateKey),
    meals: [breakfastBase, lunchBase, dinnerBase],
  };
};

const buildExerciseLogForDay = (userId, dateKey, dayIndex) => {
  const cycle = dayIndex % 28;
  const phase = Math.floor(cycle / 7);
  const cardioDuration = 16 + (cycle % 6) * 6 + phase * 2;
  const cardioCalories = 130 + (cycle % 7) * 42 + phase * 18;

  return {
    userId,
    date: dateKey,
    steps: 5200 + (cycle % 10) * 850 + phase * 320,
    workout: [
      {
        name: "Push Up",
        startTime: "07:30",
        sets: 3 + (cycle % 2),
        reps: 10 + (cycle % 4) * 2,
      },
      {
        name: "Squat",
        startTime: "18:45",
        sets: 4,
        reps: 8 + (cycle % 5),
      },
    ],
    cardio: [
      {
        name: cycle % 3 === 0 ? "Running" : cycle % 3 === 1 ? "Cycling" : "Walking",
        startTime: "06:40",
        duration: cardioDuration,
        caloriesBurned: cardioCalories,
      },
    ],
  };
};

const buildReminders = () => {
  const tomorrow = toDateKey(dateFromToday(1));
  const upcoming = toDateKey(dateFromToday(2));
  const today = toDateKey(dateFromToday(0));

  return [
    {
      title: "Morning cardio session",
      date: tomorrow,
      time: "06:30",
      category: "Health",
      leadTime: "10",
      recurring: "Everyday",
      notes: "30-minute zone 2 run before work.",
      readStatus: false,
      type: "reminder",
    },
    {
      title: "Meal prep check-in",
      date: upcoming,
      time: "20:00",
      category: "Personal",
      leadTime: "15",
      recurring: "Sunday",
      notes: "Plan next week meals and grocery list.",
      readStatus: false,
      type: "reminder",
    },
    {
      title: "Hydration reminder",
      date: today,
      time: "09:00",
      category: "General",
      leadTime: "5",
      recurring: "Everyday",
      notes: "Drink at least 500ml water this morning.",
      readStatus: false,
      type: "notification",
    },
    {
      title: "Stretch break",
      date: today,
      time: "15:00",
      category: "Work",
      leadTime: "5",
      recurring: "Monday",
      notes: "Take a quick mobility break.",
      readStatus: true,
      type: "notification",
    },
  ];
};

const seed = async () => {
  const mongoUri = process.env.MONGODB_CONNECTION_STRING;

  if (!mongoUri) {
    throw new Error("Missing MONGODB_CONNECTION_STRING in environment.");
  }

  await mongoose.connect(mongoUri);
  console.log("Connected to database.");

  let user = await User.findOne({ email: USER1_EMAIL });

  if (!user) {
    user = await User.create({
      email: USER1_EMAIL,
      password: USER1_PASSWORD,
      firstName: "Demo",
      lastName: "User",
      gender: "Male",
      dob: new Date("1996-06-15"),
      weight: 74,
      height: 176,
      activityLevel: 1.55,
      weightGoal: 0,
      dailyTargetCalorie: 2450,
      dailyTargetSteps: 9000,
      dailyTargetActivity: 40,
      profilePictureUrl:
        "https://res.cloudinary.com/demo/image/upload/v1710000000/fitpal-demo-profile.png",
      favouriteFood: [
        {
          mealId: 715538,
          foodName: "What to make for dinner tonight?? Bruschetta Style Pork & Pasta",
          imageUrl: "https://img.spoonacular.com/recipes/715538-312x231.jpg",
        },
        {
          mealId: 782585,
          foodName: "Cannellini Bean and Asparagus Salad with Mushrooms",
          imageUrl: "https://img.spoonacular.com/recipes/782585-312x231.jpg",
        },
      ],
      deactivated: false,
    });
    console.log("Created demo user.");
  } else {
    user.firstName = "Demo";
    user.lastName = "User";
    user.gender = "Male";
    user.dob = new Date("1996-06-15");
    user.weight = 74;
    user.height = 176;
    user.activityLevel = 1.55;
    user.weightGoal = 0;
    user.dailyTargetCalorie = 2450;
    user.dailyTargetSteps = 9000;
    user.dailyTargetActivity = 40;
    user.deactivated = false;
    user.favouriteFood = [
      {
        mealId: 715538,
        foodName: "What to make for dinner tonight?? Bruschetta Style Pork & Pasta",
        imageUrl: "https://img.spoonacular.com/recipes/715538-312x231.jpg",
      },
      {
        mealId: 782585,
        foodName: "Cannellini Bean and Asparagus Salad with Mushrooms",
        imageUrl: "https://img.spoonacular.com/recipes/782585-312x231.jpg",
      },
    ];
    await user.save();
    console.log("Updated existing demo user.");
  }

  let deactivatedUser = await User.findOne({ email: USER2_EMAIL });
  if (!deactivatedUser) {
    deactivatedUser = await User.create({
      email: USER2_EMAIL,
      password: USER2_PASSWORD,
      firstName: "User",
      lastName: "Two",
      gender: "Female",
      dob: new Date("1998-11-08"),
      weight: 62,
      height: 165,
      activityLevel: 1.375,
      weightGoal: -500,
      dailyTargetCalorie: 1700,
      dailyTargetSteps: 7500,
      dailyTargetActivity: 30,
      deactivated: true,
      favouriteFood: [],
    });
    console.log("Created deactivated user2 account.");
  } else {
    deactivatedUser.firstName = "User";
    deactivatedUser.lastName = "Two";
    deactivatedUser.gender = "Female";
    deactivatedUser.dob = new Date("1998-11-08");
    deactivatedUser.weight = 62;
    deactivatedUser.height = 165;
    deactivatedUser.activityLevel = 1.375;
    deactivatedUser.weightGoal = -500;
    deactivatedUser.dailyTargetCalorie = 1700;
    deactivatedUser.dailyTargetSteps = 7500;
    deactivatedUser.dailyTargetActivity = 30;
    deactivatedUser.deactivated = true;
    deactivatedUser.favouriteFood = [];
    await deactivatedUser.save();
    console.log("Updated existing user2 account as deactivated.");
  }

  const dateKeys = [];
  for (let i = PERFORMANCE_SEED_DAYS - 1; i >= 0; i--) {
    const d = dateFromToday(-i);
    dateKeys.push(toDateKey(d));
  }

  await ExerciseLog.deleteMany({ userId: user._id });
  await FoodDiary.deleteMany({ user: user._id });
  await Reminder.deleteMany({ user: user._id });
  await ExerciseLog.deleteMany({ userId: deactivatedUser._id });
  await FoodDiary.deleteMany({ user: deactivatedUser._id });
  await Reminder.deleteMany({ user: deactivatedUser._id });

  const exerciseDocs = dateKeys.map((dateKey, index) =>
    buildExerciseLogForDay(user._id, dateKey, index)
  );
  await ExerciseLog.insertMany(exerciseDocs);

  const diaryDocs = dateKeys.map((dateKey, index) => {
    const diary = buildDemoMealsForDay(dateKey, index);
    return {
      user: user._id,
      date: diary.date,
      meals: diary.meals,
    };
  });
  await FoodDiary.insertMany(diaryDocs);

  const reminders = buildReminders().map((reminder) => ({
    ...reminder,
    user: user._id,
  }));
  await Reminder.insertMany(reminders);

  console.log("Demo seed completed.");
  console.log(`User1 email: ${USER1_EMAIL}`);
  console.log(`User1 password: ${USER1_PASSWORD}`);
  console.log(`User2 email (deactivated): ${USER2_EMAIL}`);
  console.log(`User2 password: ${USER2_PASSWORD}`);
  console.log(`Seeded days: ${dateKeys.length}`);

  await mongoose.disconnect();
  console.log("Disconnected from database.");
};

seed().catch(async (error) => {
  console.error("Seed failed:", error);
  try {
    await mongoose.disconnect();
  } catch {
    // ignore disconnect errors
  }
  process.exit(1);
});
