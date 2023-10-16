import React, { useEffect, useState } from "react";
import axios from "axios";
import Header from "./Header";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Container,
  Typography,
  TextField,
  Avatar,
  IconButton,
  CardActions,
} from "@mui/material";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import Box from "@mui/material/Box";
import WhatshotIcon from "@material-ui/icons/Whatshot";
import FitnessCenterIcon from "@mui/icons-material/FitnessCenter";

const weightCardStyles = {
  weightContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  weightText: {
    fontSize: "2rem",
    fontWeight: "bold",
  },
};

function Profile(props) {
  const [targetWeight, settargetWeight] = useState("");
  const [currentTargetCalories, setTargetCalories] = useState("");
  const [currentGoal, setCurrentGoal] = useState("");
  const [editableWeight, setEditableTargetWeight] = useState(targetWeight);
  const [editableTargetCalories, setEditableTargetCalories] = useState(currentTargetCalories);
  const [editableGoal, setEditableGoal] = useState(currentGoal);

  const handleSaveInput = (e) => {
    console.log(editableWeight, editableTargetCalories, editableGoal)
    settargetWeight(editableWeight);
    setTargetCalories(editableTargetCalories);
    setCurrentGoal(editableGoal);
    console.log(targetWeight,currentTargetCalories, currentGoal)
    axios({
      method: "POST",
      url: "/goalsUpdate",
      headers: {
        Authorization: "Bearer " + props.state.token,
      },
      data: {
        targetWeight: editableWeight,
        targetCalories: editableTargetCalories,
        targetGoal: editableGoal,
      },
    })
      .then((response) => {
        const res = response.data;
        console.log(res)
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }


  const initialFirstName = "";
  const initialLastName = "";
  const initialAge = 30;
  const initialWeight = 160;
  const initialHeight = 6.0;

  const [firstName, setFirstName] = useState(initialFirstName);
  const [lastName, setLastName] = useState(initialLastName);
  const [age, setAge] = useState(initialAge);
  const [weight, setWeight] = useState(initialWeight);
  const [height, setHeight] = useState(initialHeight);

  const [profileData, setProfileData] = useState(null);

  const handleProfileSave = () => {
    // You can implement the logic here to save the values
    console.log("Saving values:",firstName, lastName, age, weight, height);
  };


  useEffect(() => {
    // Make API call to backend to get food items and their calories from DB.
    axios({
      method: "GET",
      url: "/profile",
      headers: {
        Authorization: "Bearer " + props.state.token,
      },
    })
      .then((response) => {
        const res = JSON.parse(response['data']);
        console.log(res)
        setFirstName(res.first_name)
        setLastName(res.last_name)
        setAge(res.age)
        setWeight(res.weight)
        setHeight(res.height)
        setCurrentGoal(res.target_goal)
        setTargetCalories(res.target_calories)
        settargetWeight(res.target_weight)
        setEditableGoal(res.target_goal)
        setEditableTargetCalories(res.target_calories)
        setEditableTargetWeight(res.target_weight)
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });

    }, []);


    const handleProfileSubmit = (e) => {
      console.log('height=' + height + 'weight:'+ weight)
      axios({
        method: "POST",
        url: "/profileUpdate",
        headers: {
          Authorization: "Bearer " + props.state.token,
        },
        data: {
          firstName: firstName,
          lastName: lastName,
          age: age,
          height: height,
          weight: weight
        },
      })
        .then((response) => {
          const res = response.data;
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response);
            console.log(error.response.status);
            console.log(error.response.headers);
          }
        });
    };
  return (
    <>
      <Container maxWidth>
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: 2,
            gridTemplateRows: "auto",
            gridTemplateAreas: `"profile  input input input"
                                "profile  . . ."`,
            paddingTop: "2rem",
          }}
        >
          <Card sx={{ gridArea: "profile" }} elevation={5}>
            <CardContent
              sx={{
                display: "flex",
                justifyContent: "center",
                flexDirection: "column",
              }}
            >
              {/* TODO : make profile pictures updatable */}
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-around",
                  alignItems: "center",
                  flexDirection: "column",
                  paddingBottom: "5px",
                }}
              >
                <Avatar sx={{ width: 100, height: 100 }}>
                  <AccountCircleIcon sx={{ width: 70, height: 70 }} />
                </Avatar>
                <Typography variant="h5" mt={2}>
                  Profile
                </Typography>
              </Box>
              <Box mb={2}>
                <TextField
                  label="LastName"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  fullWidth
                />
              </Box>
              <Box mb={2}>
                <TextField
                  label="FirstName"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  fullWidth
                />
              </Box>
              <Box mb={2}>
                <TextField
                  label="Age"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  fullWidth
                />
              </Box>
              <Box mb={2}>
                <TextField
                  label="Weight (lbs)"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  fullWidth
                />
              </Box>
              <Box mb={2}>
                <TextField
                  label="Height (ft)"
                  value={height}
                  onChange={(e) => setHeight(e.target.value)}
                  fullWidth
                />
              </Box>
              <Button variant="contained" color="primary" onClick={handleProfileSubmit}>
                Update  
              </Button>
            </CardContent>
          </Card>
          <Card sx={{ gridArea: "input" }} elevation={5}>
            <CardHeader
            title={"Your Goals"}
            subheader={"Update your goals here"}
            />
            {/* <CardContent
              sx={{
                display: "flex",
                justifyContent: "center",
                flexDirection: "column",
              }}
            > */}
            <CardContent
              sx={{
                display: "grid",
                gridTemplateColumns: "repeat(3, 1fr)",
                gap: 2,
                gridTemplateRows: "auto",
                gridTemplateAreas: `"targetWeight targetCalories targetGoal"
                                    ". saveButton ."`,
                paddingTop: "2rem",
              }}
            >
                <Card
                  sx={{ gridArea: "targetWeight" }}
                  elevation={2}
                >
                  <CardContent>
                    <div style={weightCardStyles.weightContainer}>
                      <IconButton
                        color="primary"
                        aria-label="weighing scale icon"
                      >
                        <FitnessCenterIcon fontSize="large" />
                      </IconButton>
                      <Typography style={weightCardStyles.weightText}>
                        {targetWeight}
                      </Typography>
                    </div>
                  </CardContent>
                  <TextField
                    label="Target Weight"
                    variant="outlined"
                    fullWidth
                    value={editableWeight}
                    onChange={(e) => setEditableTargetWeight(e.target.value)}
                  />
                </Card>
                <Card
                  sx={{ gridArea: "targetCalories" }}
                  elevation={2}
                >
                  <CardContent>
                    <div style={weightCardStyles.weightContainer}>
                      <IconButton
                        color="primary"
                        aria-label="weighing scale icon"
                      >
                        <WhatshotIcon fontSize="large" />
                      </IconButton>
                      <Typography style={weightCardStyles.weightText}>
                        {currentTargetCalories}
                      </Typography>
                    </div>
                  </CardContent>
                  <TextField
                    label="Daily Calories Burn Goal"
                    variant="outlined"
                    fullWidth
                    value={editableTargetCalories}
                    onChange={(e) => setEditableTargetCalories(e.target.value)}
                  />
                </Card>
                <Card
                  sx={{ gridArea: "targetGoal" }}
                  elevation={2}
                >
                  <CardContent>
                    <div style={weightCardStyles.weightContainer}>
                      <IconButton
                        color="primary"
                        aria-label="weighing scale icon"
                      >
                        <FitnessCenterIcon fontSize="large" />
                      </IconButton>
                      <Typography style={weightCardStyles.weightText}>
                        {currentGoal}
                      </Typography>
                    </div>
                  </CardContent>
                  <TextField
                    label="Goal"
                    variant="outlined"
                    fullWidth
                    value={editableGoal}
                    onChange={(e) => setEditableGoal(e.target.value)}
                  />
                </Card>
              <Button
                sx={{ gridArea: "saveButton" }}
                variant="contained"
                color="primary"
                // startIcon={<SaveIcon />}
                onClick={handleSaveInput}
                maxWidth
              >
                Update
              </Button>
            </CardContent>
          </Card>
        </Box>
      </Container>
    </>
  );
}

export default Profile;
