import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageGrievanceComponent } from './manage-grievance.component';

describe('ManageGrievanceComponent', () => {
  let component: ManageGrievanceComponent;
  let fixture: ComponentFixture<ManageGrievanceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ManageGrievanceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageGrievanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
