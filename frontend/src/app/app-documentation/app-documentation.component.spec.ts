import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AppDocumentationComponent } from './app-documentation.component';

describe('AppDocumentationComponent', () => {
  let component: AppDocumentationComponent;
  let fixture: ComponentFixture<AppDocumentationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppDocumentationComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AppDocumentationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
