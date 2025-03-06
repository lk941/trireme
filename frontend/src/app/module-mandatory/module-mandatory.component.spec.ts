import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModuleMandatoryComponent } from './module-mandatory.component';

describe('ModuleMandatoryComponent', () => {
  let component: ModuleMandatoryComponent;
  let fixture: ComponentFixture<ModuleMandatoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModuleMandatoryComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModuleMandatoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
