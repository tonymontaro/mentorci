/// <reference types="Cypress" />

function createStudent() {
  cy.get("#add-student").click();
  cy.get("#student-name").type("Uzi Nakamura");
  cy.get("#student-email").type("uzinaks@test.com");
  cy.get("#createStudentForm")
    .find("button")
    .click();
}

context("Home Page", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080");
    cy.get("#login-email").type("testing@test.com");
    cy.get("#login-password").type("testing000");
    cy.get("#loginForm").submit();
  });

  it("can create student", () => {
    createStudent();

    cy.get('div[testid="Uzi Nakamura"]')
      .find(".card-title")
      .should("have.text", "Uzi Nakamura");
    cy.get(".card-title").should("have.length", 1);
  });

  it("can delete student", () => {
    cy.get('div[testid="Uzi Nakamura"]')
      .find(".card-title")
      .click();
    cy.get(".fa-pencil-alt").click();
    cy.get("#deleteStudentButton").click();
    cy.get(".card-title").should("have.length", 0);
  });
});
