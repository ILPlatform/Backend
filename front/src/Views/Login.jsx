import { auth } from "../firebase";
import { signInWithEmailAndPassword, signOut } from "firebase/auth";
import React, { useState } from "react";

import { Button, Card, CardTitle, Col, Container, Form, Input, Row } from "reactstrap";

const Login = () => {
  const [state, setState] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  document.title = "Curriculum - Login";

  return (
    <div className="wrapper">
      <div
        className="page-header"
        style={
          {
            // backgroundImage: "url(" + require("assets/img/programming.jpeg").default + ")",
          }
        }
      >
        <div className="filter" />
        <Container className="mt-5 pt-5">
          <Row>
            <Col className="ml-auto mr-auto" lg="4" md="6" sm="6">
              <Card className="card-register pt-1">
                <CardTitle tag="h3">Welcome</CardTitle>
                <p className="text-center">
                  The login details are identical to the curriculum website. Note that if you are not on the whitelist
                  for the admin website, you will not be able to pass the login screen.
                </p>
                <Form
                  className="register-form"
                  onSubmit={(e) => {
                    e.preventDefault();
                    signInWithEmailAndPassword(auth, state.email, state.password)
                      .then(() => window.location.replace("/"))
                      .catch((error) => setError(error.message));
                  }}
                >
                  {error && (
                    <small className="text-danger">
                      {error}
                      <br />
                    </small>
                  )}
                  <label>Email</label>
                  <Input
                    className="no-border"
                    placeholder="Email"
                    type="email"
                    value={state.email}
                    onChange={(e) => setState({ ...state, email: e.target.value })}
                  />
                  <label>Password</label>
                  <Input
                    className="no-border"
                    placeholder="Password"
                    type="password"
                    value={state.password}
                    onChange={(e) => setState({ ...state, password: e.target.value })}
                  />
                  <Button block className="btn-round" color="danger" type="submit">
                    Log In
                  </Button>
                </Form>
              </Card>
            </Col>
          </Row>
          <div className="text-center">
            <h6>
              © {new Date().getFullYear()}
              {"  "}
              <a href="https://www.ilplatform.be" rel="noreferrer" className="text-white">
                <b>Independent Learning Platform ASBL</b>
              </a>
            </h6>
          </div>
        </Container>
      </div>
      <Button
        className="btn btn-outline-danger btn-round"
        onClick={() =>
          signOut(auth)
            .then(() => window.location.reload())
            .catch((error) => console.log(error))
        }
      >
        Sign Out
      </Button>
    </div>
  );
};

export default Login;
