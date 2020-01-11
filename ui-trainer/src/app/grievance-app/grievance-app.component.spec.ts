import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GrievanceAppComponent } from './grievance-app.component';

describe('GrievanceAppComponent', () => {
  let component: GrievanceAppComponent;
  let fixture: ComponentFixture<GrievanceAppComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GrievanceAppComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GrievanceAppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
