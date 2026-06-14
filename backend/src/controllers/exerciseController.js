import Exercise from "../models/exercise.js";
import User from "../models/user.js";
import exerciseList from "../../../frontend/src/data/exerciseList.js";
import mongoose from "mongoose";
import { format, isWithinInterval, subDays, parseISO } from "date-fns";


export const createExercise = async (req, res) => {
  const { date, steps, workout = [], cardio = [] } = req.body;
  const userId = req.userId;

  try {
    const user = await User.findById(userId);
    const weight = user?.weight || 0;

    const processedCardio = cardio.map((item) => {
      const exerciseMeta = exerciseList.find(
        (ex) => ex.name.toLowerCase() === item.name.toLowerCase()
      );

      if (!exerciseMeta) {
        console.warn("Unknown cardio activity:", item.name);
      }

      const MET = exerciseMeta?.met || 0;
      const duration = item.duration || 0;
      const caloriesBurned = (MET * 3.5 * weight * duration) / 200;

      return {
        ...item,
        caloriesBurned: Math.round(caloriesBurned),
      };
    });

    const update = {
      $push: {
        workout: { $each: workout },
        cardio: { $each: processedCardio },
      },
    };

    // Only overwrite steps if passed (avoid resetting to 0)
    if (typeof steps === "number") {
      update.$set = { steps };
    }

    const log = await Exercise.findOneAndUpdate(
      { userId, date },
      {
        $set: {
          ...(steps !== undefined ? { steps } : {}),
        },
        $push: {
          workout: { $each: workout },
          cardio: { $each: processedCardio },
        },
      },
      { upsert: true, new: true }
    );
    res.status(200).json(log);
  } catch (error) {
    console.error("Log exercise error:", error);
    res.status(500).json({ message: "Failed to save exercise log" });
  }
};

export const getExercises = async (req, res) => {
  try {
    const exercises = await Exercise.find({ userId: req.userId }).sort({
      date: -1,
    });
    res.status(200).json(exercises);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const updateTargetSteps = async (req, res) => {
  try {
    const userId = req.userId;
    const { targetSteps, workoutMinutes } = req.body;

    if (typeof targetSteps !== "number" || typeof workoutMinutes !== "number") {
      return res.status(400).json({ message: "Invalid input data" });
    }

    const user = await User.findByIdAndUpdate(
      userId,
      {
        dailyTargetSteps: targetSteps,
        dailyTargetActivity: workoutMinutes,
      },
      { new: true }
    );

    res.status(200).json(user);
  } catch (error) {
    console.error("Update daily targets error:", error);
    res.status(500).json({ message: "Server error" });
  }
};

export const logSteps = async (req, res) => {
  const { date, steps } = req.body;
  const userId = req.userId;

  if (!date || typeof steps !== "number") {
    return res.status(400).json({ message: "Invalid request data" });
  }

  try {
    const updated = await Exercise.findOneAndUpdate(
      { userId, date },
      { $set: { steps } },
      { upsert: true, new: true }
    );

    res.status(200).json(updated);
  } catch (error) {
    console.error("Log steps error:", error);
    res.status(500).json({ message: "Failed to log steps" });
  }
};

export const fetchSteps = async (req, res) => {
  try {
    const userId = req.userId;
    const today = new Date().toLocaleDateString("en-CA");

    const entry = await Exercise.findOne({ userId, date: today });

    res.json(entry || { steps: 0 });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Server error" });
  }
};

export const fetchCardioDuration = async (req, res) => {
  try {
    const userId = req.userId;
    const today = new Date().toLocaleDateString("en-CA");

    const log = await Exercise.findOne({ userId, date: today });

    if (!log || !log.cardio || log.cardio.length === 0) {
      return res.json({ totalDuration: 0 });
    }

    const totalDuration = log.cardio.reduce(
      (sum, entry) => sum + (entry.duration || 0),
      0
    );
    res.json({ totalDuration });
  } catch (error) {
    console.error("Error fetching cardio duration:", error);
    res.status(500).json({ message: "Server error" });
  }
};

export const fetchCaloriesBurned = async (req, res) => {
  try {
    const userId = req.userId;
    const today = new Date().toLocaleDateString("en-CA");

    const log = await Exercise.findOne({ userId, date: today });

    if (!log || !log.cardio || log.cardio.length === 0) {
      return res.json({ totalCalories: 0 });
    }

    const totalCalories = log.cardio.reduce(
      (sum, entry) => sum + (entry.caloriesBurned || 0),
      0
    );

    res.json({ totalCalories });
  } catch (error) {
    console.error("Error fetching calories burned:", error);
    res.status(500).json({ message: "Server error" });
  }
};

import { startOfWeek, endOfWeek } from "date-fns";

export const fetchWeeklySummary = async (req, res) => {
  try {
    const userId = req.userId;

    if (!userId) {
      return res.status(401).json({ message: "Unauthorized" });
    }

    const today = new Date();
    const start = new Date(today);
    const end = new Date(today);

    const currentDay = today.getDay();
    const mondayOffset = (currentDay === 0 ? -6 : 1) - currentDay;

    start.setDate(today.getDate() + mondayOffset);
    end.setDate(start.getDate() + 6);

    const logs = await Exercise.find({
      userId,
      date: {
        $gte: start.toISOString().split("T")[0],
        $lte: end.toISOString().split("T")[0],
      },
    });

    let totalSteps = 0;
    let totalMinutes = 0;
    let totalCalories = 0;

    logs.forEach((log) => {
      console.log("Log Date:", log.date, "Steps:", log.steps);
      totalSteps += log.steps || 0;

      const cardioMinutes =
        log.cardio?.reduce((sum, entry) => sum + (entry.duration || 0), 0) || 0;
      totalMinutes += cardioMinutes;

      const dailyCalories =
        log.cardio?.reduce((sum, entry) => sum + (entry.caloriesBurned || 0), 0) || 0;
      totalCalories += dailyCalories;
    });

    const daysCount = 7;

    console.log("Total Steps:" + totalSteps + "Day Count: " + daysCount)

    const avg = {
      averageSteps: Math.round(totalSteps / daysCount),
      averageMinutes: Math.round(totalMinutes / daysCount),
      averageCalories: Math.round(totalCalories / daysCount),
    };
    console.log(avg)

    res.json(avg);
  } catch (error) {
    console.error("Error fetching weekly summary:", error);
    res.status(500).json({ message: "Server error" });
  }
};


export const updateCardioExercise = async (req, res) => {
  try {
    const { id } = req.params;
    const updatedData = req.body;
    const userId = req.userId;

    const user = await User.findById(userId);
    const weight = user?.weight || 70;

    // Retrieve the existing exercise document to get the name
    const exerciseDoc = await Exercise.findOne({ "cardio._id": id });
    if (!exerciseDoc) {
      return res.status(404).json({ message: "Cardio exercise not found" });
    }

    // Find the cardio item by ID
    const cardioItem = exerciseDoc.cardio.find(
      (item) => item._id.toString() === id
    );
    if (!cardioItem) {
      return res.status(404).json({ message: "Cardio entry not found in document" });
    }

    const name = cardioItem.name;
    const exerciseMeta = exerciseList.find(
      (ex) => ex.name.toLowerCase() === name.toLowerCase()
    );
    const MET = exerciseMeta?.met || 0;

    const duration = updatedData.duration || 0;
    const caloriesBurned = Math.round((MET * 3.5 * weight * duration) / 200);

    const updatedExercise = await Exercise.findOneAndUpdate(
      { "cardio._id": id },
      {
        $set: {
          "cardio.$.date": updatedData.date,
          "cardio.$.startTime": updatedData.startTime,
          "cardio.$.duration": duration,
          "cardio.$.caloriesBurned": caloriesBurned,
        },
      },
      { new: true }
    );

    res.status(200).json(updatedExercise);
  } catch (error) {
    console.error("Error updating cardio exercise:", error);
    res.status(500).json({ message: "Server error" });
  }
};

export const updateWorkoutExercise = async (req, res) => {
  try {
    const { id } = req.params;
    const updatedData = req.body;

    const updatedExercise = await Exercise.findOneAndUpdate(
      { "workout._id": id },
      {
        $set: {
          "workout.$.date": updatedData.date,
          "workout.$.startTime": updatedData.startTime,
          "workout.$.sets": updatedData.sets,
          "workout.$.reps": updatedData.reps,
        },
      },
      { new: true }
    );

    if (!updatedExercise) {
      return res.status(404).json({ message: "Workout exercise not found" });
    }

    res.json(updatedExercise);
  } catch (error) {
    console.error("Error updating workout exercise:", error);
    res.status(500).json({ message: "Server error" });
  }
};

export const deleteCardioExercise = async (req, res) => {
  try {
    const { id } = req.params;

    const deletedExercise = await Exercise.findOneAndUpdate(
      { "cardio._id": id },
      { $pull: { cardio: { _id: id } } },
      { new: true }
    );

    if (!deletedExercise) {
      return res.status(404).json({ message: "Cardio exercise not found" });
    }

    res.json({
      message: "Cardio exercise deleted successfully",
      deletedExercise,
    });
  } catch (error) {
    console.error("Error deleting cardio exercise:", error);
    res.status(500).json({ message: "Server error" });
  }
};

export const deleteWorkoutExercise = async (req, res) => {
  try {
    const { id } = req.params;

    const deletedExercise = await Exercise.findOneAndUpdate(
      { "workout._id": id },
      { $pull: { workout: { _id: id } } },
      { new: true }
    );

    if (!deletedExercise) {
      return res.status(404).json({ message: "Workout exercise not found" });
    }

    res.json({
      message: "Workout exercise deleted successfully",
      deletedExercise,
    });
  } catch (error) {
    console.error("Error deleting workout exercise:", error);
    res.status(500).json({ message: "Server error" });
  }
};

export const getCalorieOutSummary = async (req, res) => {
  try {
    const { mode } = req.query;
    const userId = req.userId;

    const pipeline = [
      {
        $match: {
          userId: new mongoose.Types.ObjectId(userId),
        },
      },
      {
        $unwind: "$cardio",
      },
      {
        $addFields: {
          parsedDate: { $toDate: "$date" }, // ✅ convert string to Date
        },
      },
      {
        $group: {
          _id:
            mode === "weekly"
              ? {
                  week: { $isoWeek: "$parsedDate" },
                  year: { $isoWeekYear: "$parsedDate" },
                }
              : {
                  date: {
                    $dateToString: { format: "%Y-%m-%d", date: "$parsedDate" },
                  },
                },
          totalCaloriesOut: { $sum: "$cardio.caloriesBurned" },
        },
      },
      {
        $sort: { "_id.date": 1, "_id.week": 1 },
      },
    ];

    const result = await Exercise.aggregate(pipeline);
    res.json(result);
  } catch (err) {
    console.error("Calorie Out Error:", err.message);
    console.error(err.stack);
    res.status(500).json({ message: "Failed to summarize calories out" });
  }
};

export const getStepSummary = async (req, res) => {
  try {
    const { mode, startDate, endDate, year } = req.query;
    const userId = req.userId;

    const matchStage = {
      userId: new mongoose.Types.ObjectId(userId),
    };

    const pipeline = [{ $addFields: { parsedDate: { $toDate: "$date" } } }];

    if (mode === "daily" && startDate && endDate) {
      matchStage.date = { $gte: startDate, $lte: endDate };
      pipeline.push({ $match: matchStage });
    } else if ((mode === "weekly" || mode === "monthly") && year) {
      pipeline.push({
        $match: {
          ...matchStage,
          $expr: {
            $eq: [{ $year: "$parsedDate" }, parseInt(year)],
          },
        },
      });
    } else {
      return res.status(400).json({ message: "Invalid request" });
    }

    const groupStage =
      mode === "monthly"
        ? {
            _id: {
              month: { $month: "$parsedDate" },
              year: { $year: "$parsedDate" },
            },
            totalSteps: { $sum: "$steps" },
          }
        : mode === "weekly"
        ? {
            _id: {
              week: { $isoWeek: "$parsedDate" },
              year: { $isoWeekYear: "$parsedDate" },
            },
            totalSteps: { $sum: "$steps" },
          }
        : {
            _id: {
              date: {
                $dateToString: { format: "%Y-%m-%d", date: "$parsedDate" },
              },
            },
            totalSteps: { $sum: "$steps" },
          };

    pipeline.push({ $group: groupStage });

    pipeline.push({
      $sort:
        mode === "monthly"
          ? { "_id.month": 1 }
          : mode === "weekly"
          ? { "_id.week": 1 }
          : { "_id.date": 1 },
    });

    const result = await Exercise.aggregate(pipeline);
    res.json(result);
  } catch (error) {
    console.error("Step summary error:", error.message);
    res.status(500).json({ message: "Failed to summarize steps" });
  }
};


export const getCardioVsWorkoutSummary = async (req, res) => {
  try {
    const { mode, startDate, endDate } = req.query;
    const userId = req.userId;

    if (!mode || !startDate || !endDate) {
      return res.status(400).json({ message: "Missing query parameters" });
    }

    const pipeline = [
      {
        $match: {
          userId: new mongoose.Types.ObjectId(userId),
          date: { $gte: startDate, $lte: endDate },
        },
      },
      {
        $addFields: { parsedDate: { $toDate: "$date" } },
      },
      {
        $group: {
          _id:
            mode === "weekly"
              ? {
                  week: { $isoWeek: "$parsedDate" },
                  year: { $isoWeekYear: "$parsedDate" },
                }
              : {
                  date: {
                    $dateToString: { format: "%Y-%m-%d", date: "$parsedDate" },
                  },
                },
          totalMinutes: { $sum: { $sum: "$cardio.duration" } },
          totalReps: {
            $sum: {
              $sum: {
                $map: {
                  input: "$workout",
                  as: "w",
                  in: { $multiply: ["$$w.sets", "$$w.reps"] },
                },
              },
            },
          },
        },
      },
      {
        $sort: mode === "weekly" ? { "_id.week": 1 } : { "_id.date": 1 },
      },
    ];

    const summary = await Exercise.aggregate(pipeline);
    res.json(summary);
  } catch (error) {
    console.error("Cardio vs Workout summary error:", error);
    res.status(500).json({ message: "Failed to fetch summary" });
  }
};
