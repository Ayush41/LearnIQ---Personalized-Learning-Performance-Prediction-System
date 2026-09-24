const KEY = "learniq_user";

const ADMIN = {
  email: "abc@gmail.com",
  password: "admin123",
  name: "Admin"
};

export const DEMO = {
  email: ADMIN.email,
  password: ADMIN.password
};

export const loadUser = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY));
  } catch {
    return null;
  }
};

export async function signIn(email, password) {
  await new Promise((r) => setTimeout(r, 400));

  if (
    email.trim().toLowerCase() !== ADMIN.email ||
    password !== ADMIN.password
  ) {
    throw new Error("Email or password is incorrect.");
  }

  const user = { name: ADMIN.name, email: ADMIN.email };

  try {
    localStorage.setItem(KEY, JSON.stringify(user));
  } catch {
    // storage unavailable
  }

  return user;
}

export const signOut = () => {
  try {
    localStorage.removeItem(KEY);
  } catch {
    // storage unavailable
  }
};
