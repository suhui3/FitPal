import jwt from "jsonwebtoken";
import bcrypt from "bcryptjs";
import User from "../models/user.js";

const logIn = async (req, res) => {
  const { email, password, reactivate } = req.body;
  try {
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(404).json({ message: "Invalid Credentials" });
    }

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(404).json({ message: "Invalid Credentials" });
    }

    if (user.deactivated) {
      if (reactivate) {
        user.deactivated = false;
        await user.save();
      } else {
        return res.status(403).json({
          message: "Account is deactivated. Please reactivate to continue.",
        });
      }
    }

    const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, {
      expiresIn: "1d",
    });

    res.cookie("auth_token", token, {
      httpOnly: true,
      maxAge: 86400000,
    });

    return res.status(200).json({ userId: user._id });
  } catch (error) {
    console.log(error);
    res.status(500).json({ message: "Something went wrong" });
  }
};

const getUserId = async (req, res) => {
  return res.status(200).json({ userId: req.userId });
};

const logOut = async (req, res) => {
  res.cookie("auth_token", "", {
    expires: new Date(0),
  });
  res.send();
};

export default {
  logIn,
  getUserId,
  logOut,
};
