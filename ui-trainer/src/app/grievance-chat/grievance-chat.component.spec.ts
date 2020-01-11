import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GrievanceChatComponent } from './grievance-chat.component';

describe('GrievanceChatComponent', () => {
  let component: GrievanceChatComponent;
  let fixture: ComponentFixture<GrievanceChatComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GrievanceChatComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GrievanceChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
