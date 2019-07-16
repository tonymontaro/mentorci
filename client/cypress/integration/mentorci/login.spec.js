/// <reference types="Cypress" />

context("Login Page", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080");
  });

  it("renders login page", () => {
    cy.get("#authLink").should("have.text", "Login/Register");
  });

  it("can register and logout user", () => {
    cy.get("#loginForm")
      .find("a")
      .click();

    cy.get("#signup-email").type("testing@test.com");
    cy.get("#signup-fullname").type("Testing Stuff");
    cy.get("#signup-password").type("testing000");
    cy.get("#signupForm").submit();
    cy.get('a[href="/profile"]').click();
    cy.get("#logOutBtn").click();
  });

  it("can login user", () => {
    cy.get("#login-email").type("testing@test.com");
    cy.get("#login-password").type("testing000");
    cy.get("#loginForm").submit();
  });
});
