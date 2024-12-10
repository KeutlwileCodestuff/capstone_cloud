
async function signUp(username, password, email) {
  try {
    const user = await Auth.signUp({
      username,
      password,
      attributes: {
        email, 
      },
    });
    console.log('Sign-Up successful:', user);
  } catch (error) {
    console.error('Error signing up:', error);
  }
}


async function signIn(username, password) {
    try {
      const user = await Auth.signIn(username, password);
      console.log('User signed in:', user);
    } catch (error) {
      console.error('Error signing in:', error);
    }
  }
