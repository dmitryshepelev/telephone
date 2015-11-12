ALTER TABLE "main_app_userprofile" ADD COLUMN "secret_key" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "secret_key" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "user_code" TYPE varchar(30);

ALTER TABLE "main_app_userprofile" DROP COLUMN "user_code" CASCADE;
ALTER TABLE "main_app_userprofile" ADD COLUMN "profile_email" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "profile_email" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "profile_password" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "profile_password" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "token" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "token" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "uid" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "uid" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "user_key" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "user_key" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "secret_key" TYPE varchar(50);

ALTER TABLE "main_app_userprofile" DROP CONSTRAINT "main_app_userp_schema_id_4cddfcbff18e38b1_fk_main_app_schema_id";
ALTER TABLE "main_app_userprofile" DROP COLUMN "schema_id" CASCADE;
DROP TABLE "main_app_schema" CASCADE;

-- Create call teble - 15.10.2015 --
CREATE TABLE "main_app_call" (
	"id" serial NOT NULL PRIMARY KEY,
	"call_id" varchar(30) NOT NULL,
	"sip" varchar(20) NULL,
	"date" timestamp with time zone NULL,
	"destination" varchar(30) NULL,
	"description" varchar(100) NULL,
	"disposition" varchar(20) NULL,
	"bill_seconds" integer NULL,
	"cost" double precision NULL,
	"bill_cost" double precision NULL,
	"currency" varchar(20) NULL,
	"user_profile_id" integer NOT NULL);
ALTER TABLE "main_app_call" ADD CONSTRAINT "main_app_ca_user_profile_id_586a6b3e_fk_main_app_userprofile_id" FOREIGN KEY ("user_profile_id") REFERENCES "main_app_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "main_app_call_06037614" ON "main_app_call" ("user_profile_id");

ALTER TABLE "main_app_call" ADD COLUMN "is_answered" boolean DEFAULT true NOT NULL;
ALTER TABLE "main_app_call" ALTER COLUMN "is_answered" DROP DEFAULT;

CREATE TABLE "main_app_callee" ("id" serial NOT NULL PRIMARY KEY, "sip" varchar(20) NOT NULL UNIQUE, "description" varchar(100) NULL, "first_call_date" timestamp with time zone NULL);
ALTER TABLE "main_app_call" DROP COLUMN "description" CASCADE;
ALTER TABLE "main_app_call" DROP COLUMN "sip" CASCADE;
ALTER TABLE "main_app_call" ADD COLUMN "callee_id" integer NOT NULL;
CREATE INDEX "main_app_callee_sip_38a802ef_like" ON "main_app_callee" ("sip" varchar_pattern_ops);
CREATE INDEX "main_app_call_56286df8" ON "main_app_call" ("callee_id");
ALTER TABLE "main_app_call" ADD CONSTRAINT "main_app_call_callee_id_70a0e395_fk_main_app_callee_id" FOREIGN KEY ("callee_id") REFERENCES "main_app_callee" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "main_app_call" ADD COLUMN "record_filename" varchar(100) NULL;
ALTER TABLE "main_app_callee" ALTER COLUMN "description" TYPE varchar(1000);
-- --

-- 30.10.2015 Added Customer number --
ALTER TABLE "main_app_userprofile" ADD COLUMN "customer_number" varchar(10) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "customer_number" DROP DEFAULT;
-- --

-- 02.10.2015 Added SubscribeTransaction, TransactionStatus tables --
CREATE TABLE "main_app_subscribetransaction" ("id" serial NOT NULL PRIMARY KEY, "transact_id" varchar(40) NOT NULL, "receiver" varchar(20) NOT NULL, "form_comments" varchar(50) NULL, "short_dest" varchar(50) NULL, "quickpay_form" varchar(6) NOT NULL, "targets"
varchar(150) NULL, "sum" double precision NOT NULL, "payment_type" varchar(2) NOT NULL, "duration" integer NOT NULL, "expiration_date" timestamp with time zone NULL);
CREATE TABLE "main_app_transactionstatus" ("id" serial NOT NULL PRIMARY KEY, "value" varchar(20) NOT NULL);
ALTER TABLE "main_app_subscribetransaction" ADD COLUMN "status_id" integer NOT NULL;
ALTER TABLE "main_app_subscribetransaction" ALTER COLUMN "status_id" DROP DEFAULT;
ALTER TABLE "main_app_subscribetransaction" ADD COLUMN "user_profile_id" integer NOT NULL;
ALTER TABLE "main_app_subscribetransaction" ALTER COLUMN "user_profile_id" DROP DEFAULT;
CREATE INDEX "main_app_subscribetransaction_dc91ed4b" ON "main_app_subscribetransaction" ("status_id");
ALTER TABLE "main_app_subscribetransaction" ADD CONSTRAINT "main_app_su_status_id_5f99843b_fk_main_app_transactionstatus_id" FOREIGN KEY ("status_id") REFERENCES "main_app_transactionstatus" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "main_app_subscribetransaction_06037614" ON "main_app_subscribetransaction" ("user_profile_id");
ALTER TABLE "main_app_subscribetransaction" ADD CONSTRAINT "main_app_su_user_profile_id_3b9379c6_fk_main_app_userprofile_id" FOREIGN KEY ("user_profile_id") REFERENCES "main_app_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "main_app_subscribetransaction" ADD COLUMN "creation_date" timestamp with time zone DEFAULT now() NOT NULL;
ALTER TABLE "main_app_subscribetransaction" ALTER COLUMN "creation_date" DROP DEFAULT;
ALTER TABLE "main_app_subscribetransaction" ADD COLUMN "is_archive" boolean DEFAULT false NOT NULL;
ALTER TABLE "main_app_subscribetransaction" ALTER COLUMN "is_archive" DROP DEFAULT;

ALTER TABLE "main_app_userprofile" ADD COLUMN "date_subscribe_ended" timestamp with time zone NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "date_subscribe_ended" DROP DEFAULT;

ALTER TABLE "main_app_userprofile" ADD COLUMN "profile_phone_number" varchar(20) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "profile_phone_number" DROP DEFAULT;


-- --


