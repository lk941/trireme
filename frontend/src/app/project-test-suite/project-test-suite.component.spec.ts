import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectTestSuiteComponent } from './project-test-suite.component';

describe('ProjectTestSuiteComponent', () => {
  let component: ProjectTestSuiteComponent;
  let fixture: ComponentFixture<ProjectTestSuiteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProjectTestSuiteComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ProjectTestSuiteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
