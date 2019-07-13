/// <reference types="Cypress" />

context("Home Page", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080");
    cy.get("#login-email").type("testing@test.com");
    cy.get("#login-password").type("testing000");
    cy.get("#loginForm").submit();
  });

  it("can create student", () => {
    cy.get("#add-student").click();
    cy.get("#student-name").type("Uzi Nakamura");
    cy.get("#student-email").type("uzinaks@test.com");
    cy.get("#createStudentForm")
      .find("button")
      .click();
  });
});
