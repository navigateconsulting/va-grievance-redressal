import { Component, OnInit } from '@angular/core';
import { SharedDataService } from '../common/services/shared-data.service';
import { constant } from '../../environments/constants';
import { WebSocketService } from '../common/services/web-socket.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-grievance-chat',
  templateUrl: './grievance-chat.component.html',
  styleUrls: ['./grievance-chat.component.scss']
})
export class GrievanceChatComponent implements OnInit {

  grievance_id: string;
  chats: Array<object>;
  grievance_json: Array<object>;

  constructor(public webSocketService: WebSocketService,
              public sharedDataService: SharedDataService,
              public _router: Router) { }

  ngOnInit() {
    this.grievance_id = this.sharedDataService.getSharedData('grievance_id', constant.MODULE_COMMON);
    if (Object.keys(this.grievance_id).length === 0) {
      this._router.navigate(['/home/grievance']);
    } else {
      this.grievance_json = new Array<object>();
      this.grievance_json = this.sharedDataService.getSharedData('grievance_json', constant.MODULE_COMMON)[0];
      delete this.grievance_json['_id'];
      delete this.grievance_json['sender_id'];
      this.getGrievanceChat();
    }
  }

  getGrievanceChat() {
    this.chats = new Array<object>();
    this.webSocketService.createGrievanceRoom('agrievance');
    this.webSocketService.getAGrievance('agrievance', this.grievance_id).subscribe(agrievance => {
      this.chats = agrievance['events'];
    },
    err => console.error('Observer got an error: ' + err),
    () => console.log('Observer got a complete notification'));
  }

}
