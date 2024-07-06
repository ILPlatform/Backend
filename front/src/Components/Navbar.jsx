import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Button, Collapse, Container, Nav, Navbar, NavbarBrand, NavItem, NavLink } from "reactstrap";
import { auth } from "../firebase";
import { onAuthStateChanged, signOut } from "firebase/auth";

const NavBar = () => {
  const [bodyClick, setBodyClick] = useState(false);
  const [collapseOpen, setCollapseOpen] = useState(false);
  const [name, setName] = useState("");

  onAuthStateChanged(auth, (user) => setName(user?.email));

  return (
    <>
      {bodyClick ? (
        <div
          id="bodyClick"
          onClick={() => {
            document.documentElement.classList.toggle("nav-open");
            setBodyClick(false);
            setCollapseOpen(false);
          }}
        />
      ) : null}
      <Navbar className="fixed-top pt-0 navbar-light" id="navbar-main" expand="lg">
        <Container className="d-flex">
          <NavbarBrand id="navbar-brand" to="/" className="py-2" tag={Link}>
            <img src={require("../assets/img/ILPlatform_Banner.png")} style={{ height: "50px" }} alt="ILPlatform" />
          </NavbarBrand>
          <button
            className="navbar-toggler"
            id="navigation"
            type="button"
            onClick={() => {
              document.documentElement.classList.toggle("nav-open");
              setBodyClick(true);
              setCollapseOpen(true);
            }}
          >
            <span className="navbar-toggler-bar bar1"></span>
            <span className="navbar-toggler-bar bar2"></span>
            <span className="navbar-toggler-bar bar3"></span>
          </button>
          <Collapse navbar isOpen={collapseOpen} className="justify-content-end">
            <Nav className="mr-auto" navbar>
              {/* <NavItem>
                <NavLink href="/">Home</NavLink>
              </NavItem> */}
              <p className="my-auto">Signed in as {name}</p>
              <Button
                className="btn btn-outline-danger btn-round mx-2"
                onClick={() =>
                  signOut(auth)
                    .then(() => window.location.reload())
                    .catch((error) => console.log(error))
                }
              >
                Sign Out
              </Button>
            </Nav>
          </Collapse>
        </Container>
      </Navbar>
    </>
  );
};

export default NavBar;
